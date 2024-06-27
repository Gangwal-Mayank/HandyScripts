import jenkins.model.*
import hudson.model.ModelObject
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey
import com.cloudbees.jenkins.plugins.awscredentials.AWSCredentialsImpl
import org.jenkinsci.plugins.plaincredentials.StringCredentials
import org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl
import com.cloudbees.hudson.plugins.folder.Folder
import groovy.xml.MarkupBuilder

class DeepCredentialsPrinter {

  private static final boolean DEBUG = false;

  private final out;
  private final Set<CredentialsStore> visitedStores = new HashSet<>();

  DeepCredentialsPrinter(out) {
      this.out = out;
  }

  private void start() {
    process(Jenkins.getInstance())
  }

  private void process(ItemGroup group) {
    def root = new MarkupBuilder(out)
    root.records {
      printCreds(group, root)
    }

    List<ItemGroup> items = group.getItems();
    if (items == null || items.isEmpty()) {
      return;
    }

    for (item in items) {
      if (item instanceof ItemGroup) {
        process(item);
      } else if (item instanceof Item) {
        printCreds(item, root)
      } else {
        if (DEBUG) {
          out.println("[DEBUG] unsupported item type: " + item.getClass().getCanonicalName());
        }
      }
    }
  }

  private void printCreds(ModelObject model, MarkupBuilder builder) {
    for (store in CredentialsProvider.lookupStores(model)) {
      if (visitedStores.add(store)) { // only visit new stores
        print(model.getFullName(), store.getCredentials(Domain.global()), builder);
      }
    }
  }

  private void print(String fullname, List<Credentials> creds, MarkupBuilder builder) {
    if (creds.isEmpty()) {
      if (DEBUG) {
        out.println("[DEBUG] No credentials in /" + fullname);
      }
    } else {
      creds.each { c ->
        builder.record {
          if (fullname)
            folder("Folder: /$fullname")
          id("id: ${c.id}")
          if (c.properties.description) {
            description("description: ${c.description}")
          }
          if (c.properties.username) {
            username("username: ${c.username}")
          }
          if (c.properties.password) {
            password("password: ${c.password}")
          }
          if (c.properties.passphrase) {
            passphrase("passphrase: ${c.passphrase}")
          }
          if (c.properties.secret) {
            secret("secret: ${c.secret}")
          }
          if (c.properties.secretBytes) {
            secretBytes("secretBytes: ${new String(c.secretBytes.getPlainData())}")
          }
          if (c.properties.privateKeySource) {
            privateKey("privateKey: ${c.getPrivateKey()}")
          }
          if (c.properties.apiToken) {
            apiToken("apiToken: ${c.apiToken}")
          }
          if (c.properties.token) {
            token("token: ${c.token}")
          }
        }
      }
    }
  }
}

def writer = new StringWriter()
new DeepCredentialsPrinter(writer).start()
println(writer.toString())
