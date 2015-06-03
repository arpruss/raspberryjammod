package mobi.omegacentauri.rjm;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.net.Uri;
import android.os.Build;

public class MarketDetector {
	public static final int MARKET = 0;
	public static final int APPSTORE = 1;
	public static final String[] marketNames = { "Play", "Appstore" };

	public static void launch(Context c) {
    	Intent i = new Intent(Intent.ACTION_VIEW);
    	i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    	if (detect(c) == MARKET)
    		i.setData(Uri.parse("market://details?id=mobi.omegacent"+"auri.rjm"));
    	else
    		i.setData(Uri.parse("http://www.amazon.com/gp/mas/dl/android?p=mobi.omegacent"+"auri.red_pro"));            		
    	c.startActivity(i);    	
	}
	
	public static String getStoreLink(Context c) {
		if (detect(c) != APPSTORE) {
			//    	String store = "https://play.google.com/store/apps/details?id=";
			return "market://details?id=";
		}
		else {
			return "http://www.amazon.com/gp/mas/dl/android?p=";
		}
	}
	
	public static int detect(Context c) {
		PackageManager pm = c.getPackageManager();
				
		String installer = pm.getInstallerPackageName(c.getPackageName());
		
		if (installer != null && installer.equals("com.android.vending")) 
			return MARKET;
		
		if (Build.MODEL.equalsIgnoreCase("Kindle Fire")) 
			return APPSTORE;

		try {
			if (pm.getPackageInfo("com.amazon.venezia", 0) != null) 
				return APPSTORE;
		} catch (NameNotFoundException e) {
		}
		
		return MARKET;
	}
	
	public static String getMarketName(Context c) {
		return marketNames[detect(c)];
	}
}
