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
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.res.AssetManager;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.preference.PreferenceManager;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Comparator;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import mobi.omegacentauri.rjm.R;

public class MainActivity extends Activity {
	private SharedPreferences options;
	private Spinner pythonVersionSpinner;
	private Spinner overwriteModeSpinner;

	static final String SCRIPTS2 = "/com.hipipal.qpyplus/scripts"; 
	static final int PYTHON2 = 0;
//	static final int PYTHON3 = 1;
	static final int OVERWRITE_NO = 0;
	static final int OVERWRITE_YES = 1;
	static final int OVERWRITE_DELETE = 2;
	static final int OVERWRITE_ONLY_MOD = 3;
//	public static final String PREF_PYTHON_VERSION = "pythonVersion";
	public static final String PREF_OVERWRITE_MODE = "overwriteMode";

	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        options = PreferenceManager.getDefaultSharedPreferences(this);
        setContentView(R.layout.main);
//        pythonVersionSpinner = (Spinner)findViewById(R.id.python_version);
//        pythonVersionSpinner.setSelection(options.getInt(PREF_PYTHON_VERSION, PYTHON2));
//        pythonVersionSpinner.setOnItemSelectedListener(new OnItemSelectedListener() {
//			@Override
//			public void onItemSelected(AdapterView<?> arg0, View arg1,
//					int pos, long arg3) {
//				options.edit().putInt(PREF_PYTHON_VERSION, pos).commit();
//				showInstructions();
//			}
//
//			@Override
//			public void onNothingSelected(AdapterView<?> arg0) {
//			}
//		});
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
    
    public void showInstructions() {
    	TextView tv = (TextView)findViewById(R.id.instructions);
    	tv.setMovementMethod(LinkMovementMethod.getInstance());
    	
    	String message = "";
    	
    	String store = MarketDetector.getStoreLink(this);
    	
    	boolean haveMinecraft;

    	try {
			haveMinecraft = null != getPackageManager().getPackageInfo("com.mojang.minecraftpe", 0);
		} catch (NameNotFoundException e) {
			haveMinecraft = false;
		}
    	
    	boolean haveAll = true;    	
    	
    	if (haveMinecraft) {
    		message += "<p>1. You have Minecraft PE installed. Excellent!</p>";
    	}
    	else {
			message += "<p>1. Install <a href='"+store+"com.mojang.minecraftpe'>Minecraft PE</a>.</p>";
			haveAll = false;
    	}

    	String qpythonReadable;
    	String qpythonPackage;
//    	if (options.getInt(PREF_PYTHON_VERSION, PYTHON2) == PYTHON2) {
    		qpythonReadable = "QPython";
    		qpythonPackage = "com.hipipal.qpyplus";
//    	}
//    	else {
//    		qpythonReadable = "QPython3";
//    		qpythonPackage = "com.hipipal.qpy3";
//    	}
    	
    	boolean haveQPython;
    	
		try {
			haveQPython = null != getPackageManager().getPackageInfo(qpythonPackage, 0);
		} catch (NameNotFoundException e) {
			haveQPython = false;
		}
		
		if (haveQPython) {
			message += "<p>2. You have "+qpythonReadable+" installed. Excellent!</p>";
		}
		else {
			message += "<p>2. Install <a href='"+store+qpythonPackage+"'>"+qpythonReadable+"</a>.</p>";
			haveAll = false;
		}
		
		try {
			haveQPython = null != getPackageManager().getPackageInfo(qpythonPackage, 0);
		} catch (NameNotFoundException e) {
			haveQPython = false;
		}

		String bl = null;
		boolean haveBLPro;
		try {
			haveBLPro = null != getPackageManager().getPackageInfo("net.zhuoweizhang.mcpelauncher.pro", 0);
		} catch (NameNotFoundException e) {
			haveBLPro = false;
		}
		
		if (haveBLPro) {
			bl = "BlockLauncher Pro";
		}
		else {
			boolean haveBL;
			try {
				haveBL = null != getPackageManager().getPackageInfo("net.zhuoweizhang.mcpelauncher", 0);
			} catch (NameNotFoundException e) {
				haveBL = false;
			}
			
			if (haveBL) {
				bl = "BlockLaucher";
			}
		}
		
		if (bl == null) {
			message += "<p>3. Install <a href='"+store+"net.zhuoweizhang.mcpelauncher.pro'>BlockLauncher Pro</a> or the free "+
					"<a href='"+store+"net.zhuoweizhang.mcpelauncher'>BlockLauncher</a>.</p>";
			bl = "BlockLauncher";
			haveAll = false;
		} 
		else {
			message += "<p>3. You have "+bl+" installed. Excellent!</p>"; 	
		}
		
		message += "<p>4. Tap on the 'Install' button and agree to install mod." + (haveAll?"":" (The button will show up once the above steps are done.)")+"</p>";

		tv.setText(Html.fromHtml(message));
		
		ViewGroup install = (ViewGroup)findViewById(R.id.install);
		install.setVisibility(haveAll ? View.VISIBLE : View.INVISIBLE);
    	tv = (TextView)findViewById(R.id.instructions2);
		message = "";		
		message += "<p>5. Go to "+bl+", make sure screen is in landcape mode (it may crash in portrait) and tap on the wrench button.</p>";
		message += "<p>6. Choose 'Manage ModPE Scripts', then tap on 'raspberryjampe.js'.</p>";
		message += "<p>7. Tap on 'enable'.</p>";
		message += "<p>8. Press BACK and then start Minecraft PE inside BlockLauncher with 'Play'.</p>";
		message += "<p>9. Switch between Minecraft and QPython to run scripts.</p>";
		tv.setText(Html.fromHtml(message));		
    }
    
    @Override
    public void onResume() {
    	super.onResume();
    	showInstructions();
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
    	if (overwriteMode == OVERWRITE_ONLY_MOD || ( overwriteMode == OVERWRITE_NO && out.exists()) )
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
			String scriptDir = rootDir+SCRIPTS2;
			String pyVer = "2";
//			if (options.getInt(PREF_PYTHON_VERSION, PYTHON2) == PYTHON3) {
//				scriptDir += "3";
//				pyVer = "3";
//			}
			int overwrite = options.getInt(PREF_OVERWRITE_MODE, OVERWRITE_YES);
			File base = new File(scriptDir);
			if (overwrite == OVERWRITE_DELETE) {
				publishProgress("Cleaning");
				recursiveDelete(base);
			}
			base.mkdirs();
			AssetManager assets = context.getAssets();
						
			ZipInputStream zip = null;
			
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
						copyStreamToFile(zip, out, entry.getName().endsWith(".js") ? OVERWRITE_YES : overwrite);
					}
				}
			} catch(IOException e) {
				return false;
			} finally {
				if (zip != null)
					try {
						zip.close();
					} catch (IOException e) {
					}
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
				Intent intent = new Intent("net.zhuoweizhang.mcpelauncher.action.IMPORT_SCRIPT");
				String path = Environment.getExternalStorageDirectory().getPath()+"/"+SCRIPTS2+"/"+"raspberryjampe.js";
				intent.setDataAndType(Uri.fromFile(new File(path)), "text/plain");			
				context.startActivity(intent);
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