import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.widget.Toast;

public class MyActivity extends Activity {

	protected void Test() {
		Intent intent = new Intent(this, BPSplashActivity.class);
		intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

		startActivity(intent);

	}

	protected void Test2() {
		Intent intent = new Intent(this, BPSplashActivity.class);
		intent.addFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK);

		startActivity(intent);

	}

}