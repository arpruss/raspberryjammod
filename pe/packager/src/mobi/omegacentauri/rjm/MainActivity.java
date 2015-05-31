package mobi.omegacentauri.rjm;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;

import android.app.Activity;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.preference.PreferenceManager;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Toast;

import java.util.Comparator;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class MainActivity extends Activity {
	private SharedPreferences options;
	private Spinner pythonVersionSpinner;
	private Spinner overwriteModeSpinner;
	
	static final int PYTHON2 = 0;
	static final int PYTHON3 = 1;
	static final int OVERWRITE_NO = 0;
	static final int OVERWRITE_YES = 1;
	static final int OVERWRITE_DELETE = 2;
	public static final String PREF_PYTHON_VERSION = "pythonVersion";
	public static final String PREF_OVERWRITE_MODE = "overwriteMode";

	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        options = PreferenceManager.getDefaultSharedPreferences(this);
        setContentView(R.layout.main);
        pythonVersionSpinner = (Spinner)findViewById(R.id.python_version);
        pythonVersionSpinner.setSelection(options.getInt(PREF_PYTHON_VERSION, PYTHON2));
        pythonVersionSpinner.setOnItemSelectedListener(new OnItemSelectedListener() {
			@Override
			public void onItemSelected(AdapterView<?> arg0, View arg1,
					int pos, long arg3) {
				options.edit().putInt(PREF_PYTHON_VERSION, pos).commit();
			}

			@Override
			public void onNothingSelected(AdapterView<?> arg0) {
			}
		});
        overwriteModeSpinner = (Spinner)findViewById(R.id.overwrite_mode);
        overwriteModeSpinner.setSelection(options.getInt(PREF_OVERWRITE_MODE, OVERWRITE_YES));
        overwriteModeSpinner.setOnItemSelectedListener(new OnItemSelectedListener() {
			@Override
			public void onItemSelected(AdapterView<?> arg0, View arg1,
					int pos, long arg3) {
				options.edit().putInt(PREF_OVERWRITE_MODE, pos).commit();
			}

			@Override
			public void onNothingSelected(AdapterView<?> arg0) {
			}
		});
    }
    
    public void onInstall(View v) {
    	new InstallerTask(this).execute();
    }
    
    @Override
    public void onResume() {
    	super.onResume();
    }

    static void recursiveDelete(File branch) {
    	if (! branch.exists())
    		return;
    	if (! branch.isDirectory()) {
    		branch.delete();
    		return;
    	}
    	for (File leaf : branch.listFiles()) {
    		recursiveDelete(leaf);
    	}
    }
    
    static void copyStreamToFile(InputStream in, File out, int overwriteMode) throws IOException {
    	if (overwriteMode == OVERWRITE_NO && out.exists())
    		return;
		byte[] buffer = new byte[16384];
		FileOutputStream outStream = new FileOutputStream(out);
		int didRead;
		while (0 <= (didRead = in.read(buffer))) {
			outStream.write(buffer,0,didRead);
		}			
		outStream.close();
    }

	static class InstallerTask extends AsyncTask<Void, String, Boolean> {
		final Context	 context;
		ProgressDialog progress;
		SharedPreferences options;

		InstallerTask(Context c) {
			context = c;
			options = PreferenceManager.getDefaultSharedPreferences(context);
		}

		@Override
		protected Boolean doInBackground(Void... opt) {
			String rootDir = Environment.getExternalStorageDirectory().getPath();
			String scriptDir = rootDir+"/com.hipipal.qpyplus/scripts";
			String pyVer = "2";
			if (options.getInt(PREF_PYTHON_VERSION, PYTHON2) == PYTHON3) {
				scriptDir += "3";
				pyVer = "3";
			}
			int overwrite = options.getInt(PREF_OVERWRITE_MODE, OVERWRITE_YES);
			File base = new File(scriptDir);
			if (overwrite == OVERWRITE_DELETE) {
				publishProgress("Cleaning");
				recursiveDelete(base);
			}
			base.mkdirs();
			AssetManager assets = context.getAssets();
			
			publishProgress("Copying mod to "+rootDir);
			InputStream in = null;
			try {
				in = assets.open("droidjam.js");
				copyStreamToFile(in, new File(rootDir + "/droidjam.js"), OVERWRITE_YES);
			} catch (IOException e) {
				return false;
			} finally {
				if (in != null) {
					try {
						in.close();
					}
					catch (Exception e) {}
				}
			}
			
			ZipInputStream zip;
			
			try {
				zip = new ZipInputStream(assets.open("p" + pyVer + ".zip"));
				ZipEntry entry;
				
				while (null != (entry = zip.getNextEntry())) {
					publishProgress("Copying "+entry.getName());
					File out = new File(scriptDir + "/" + entry.getName());
					if (entry.isDirectory()) {
						out.mkdirs();
					}
					else {
						out.getParentFile().mkdirs();
						copyStreamToFile(zip, out, overwrite);
					}
				}
			} catch(IOException e) {
				return false;
			} finally {
			}
			
			return true;
		}

		@Override
		protected void onProgressUpdate(String... message) {
			if (progress != null) {
				progress.setMessage(message[0]);
			}

		}

		@Override
		protected void onPreExecute() {
			progress = ProgressDialog.show(context, "", "Installing", true, false);
			progress.setCancelable(false);
		}

		@Override
		protected void onPostExecute(Boolean success) {
			if (success != null && success) {
				Toast.makeText(context, "Scripts and mod ready", Toast.LENGTH_SHORT).show();
			}
			else {
				Toast.makeText(context, "Failed!", Toast.LENGTH_LONG).show();
			}

			try {
				progress.dismiss();
			}
			catch (Exception e) {					
			}
		}
	}
}