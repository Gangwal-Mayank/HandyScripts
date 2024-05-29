boolean dryRun = false;
long cutoffHours = 24

/* Remove Queue Items with incorrect Node Label */

queueItems = Jenkins.instance.queue.items

queueItems.each({
  if (it instanceof hudson.model.Queue.BuildableItem && it.getWhy().startsWith("There are no nodes with the label")) {
    println("Let's remove this from the queue: " + it.toString() + " Because it has an invalid label: " + it.getAssignedLabel().name)
  	if (!dryRun) {
  	    Jenkins.instance.queue.cancel(it)
  	}
  }
})

/* Remove long running job builds */

import org.jenkinsci.plugins.workflow.job.WorkflowRun
import org.jenkinsci.plugins.workflow.support.steps.ExecutorStepExecution

WorkflowRun getPipelineRunFromExecutable(hudson.model.Executor exec) {
  if (exec.isBusy() && exec.currentExecutable) {
    if (exec.currentExecutable instanceof WorkflowRun) {
        return ((WorkflowRun) exec.currentExecutable)
    }

    if (exec.currentExecutable.parent instanceof ExecutorStepExecution.PlaceholderTask) {
        def executorPlaceholderTask = ((ExecutorStepExecution.PlaceholderTask) exec.currentExecutable.parent)
        return ((WorkflowRun) executorPlaceholderTask.runForDisplay())
    }
  }
  else {
    return null
  }
}

runningBuilds = Jenkins.instance.getComputers().collect { computer -> computer.executors.collect { exec -> getPipelineRunFromExecutable(exec) }
}.flatten()

runningBuilds.removeAll([null])

long currentTime = System.currentTimeMillis()
long hour = 60 * 60 * 1000
long cutoff = cutoffHours * hour

runningBuilds.each {
  long duration = currentTime - it.getStartTimeInMillis()
  if (duration > cutoff) {
    println(it.getAbsoluteUrl())
    if (!dryRun) {
      it.doKill()
    }
  }
}

/* Remove jobs that failed to execute after restart */

def searchStringInLogBuild(build, string, dryRun) {
  BufferedReader reader = null
  HashSet<String> uniqueReadyToRuns = new HashSet<>();
  boolean lastLineProximity = false;
  int lastLineProximityThreshold = 3;
  int countLinesSince = lastLineProximityThreshold + 1;
  try {
    reader = new BufferedReader(build?.getLogReader());
    for (String line = reader.readLine(); line != null; line = reader.readLine()) {
      if (line =~ string) {
        uniqueReadyToRuns.add(line)
        countLinesSince = 0;
      }
      else {
        countLinesSince++;
      }
    }
  } catch (Exception e) {
    println("Error: " + e);
  } finally {
    if (reader != null) {
      reader.close();
    }
  }
  lastLineProximity = countLinesSince < lastLineProximityThreshold; // Is the "Ready to run at" at the bottom of the script?
  if (uniqueReadyToRuns.size() > 1 && lastLineProximity) {
    println("Build being executed and it's going to be killed: " + build.getAbsoluteUrl() + " Number of Ready to Runs: " + uniqueReadyToRuns.size() + " Distance from Bottom: " + countLinesSince)
    if (!dryRun) {
      build.doKill()
    }
  }
}

runningBuilds.each { build ->
    searchStringInLogBuild(build, "Ready to run at", dryRun)
}


return null
