package org.owasp.goatdroid.fourgoats.db;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteStatement;
import android.util.Log;
import java.util.ArrayList;
import java.util.HashMap;

public class CheckinDBHelper
{
  private static final String AUTO_CHECKIN_TABLE = "autocheckin";
  private static final String CHECKINS_TABLE_NAME = "checkins";
  private static final String DATABASE_NAME = "checkins.db";
  private static final int DATABASE_VERSION = 1;
  private static final String INSERT_AUTO_CHECKIN = "insert into autocheckin (latitude, longitude, dateTime) values (?,?,?)";
  private static final String INSERT_CHECKIN = "insert into checkins (checkinID, venueName, dateTime, latitude, longitude) values (?,?,?,?,?)";
  private Context context;
  private SQLiteDatabase db;
  private SQLiteStatement insertAutoCheckinStmt;
  private SQLiteStatement insertStmt;
  
  public CheckinDBHelper(Context paramContext)
  {
    this.context = paramContext;
    this.db = new CheckinOpenHelper(this.context).getWritableDatabase();
    this.insertStmt = this.db.compileStatement("insert into checkins (checkinID, venueName, dateTime, latitude, longitude) values (?,?,?,?,?)");
    this.insertAutoCheckinStmt = this.db.compileStatement("insert into autocheckin (latitude, longitude, dateTime) values (?,?,?)");
  }
  
  public void close()
  {
    this.db.close();
  }
  
  public ArrayList<HashMap<String, String>> getCheckins()
  {
    Cursor localCursor = this.db.query("checkins", new String[] { "checkinID", "venueName", "dateTime", "latitude", "longitude" }, null, null, null, null, null);
    ArrayList localArrayList = new ArrayList();
    HashMap localHashMap = new HashMap();
    for (;;)
    {
      if (!localCursor.moveToNext()) {
        return localArrayList;
      }
      localHashMap.put("checkinID", localCursor.getString(localCursor.getColumnIndex("checkinID")));
      localHashMap.put("venueName", localCursor.getString(localCursor.getColumnIndex("venueName")));
      localHashMap.put("dateTime", localCursor.getString(localCursor.getColumnIndex("dateTime")));
      localHashMap.put("latitude", localCursor.getString(localCursor.getColumnIndex("latitude")));
      localHashMap.put("longitude", localCursor.getString(localCursor.getColumnIndex("longitude")));
      localArrayList.add(localHashMap);
    }
  }
  
  public void insertAutoCheckin(String paramString1, String paramString2, String paramString3)
  {
    this.insertAutoCheckinStmt.bindString(1, paramString1);
    this.insertAutoCheckinStmt.bindString(2, paramString2);
    this.insertAutoCheckinStmt.bindString(3, paramString3);
    this.insertAutoCheckinStmt.executeInsert();
  }
  
  public void insertCheckin(HashMap<String, String> paramHashMap)
  {
    this.insertStmt.bindString(1, (String)paramHashMap.get("checkinID"));
    this.insertStmt.bindString(2, (String)paramHashMap.get("venueName"));
    this.insertStmt.bindString(3, (String)paramHashMap.get("dateTime"));
    this.insertStmt.bindString(4, (String)paramHashMap.get("latitude"));
    this.insertStmt.bindString(5, (String)paramHashMap.get("longitude"));
    this.insertStmt.executeInsert();
  }
  
  private class CheckinOpenHelper
    extends SQLiteOpenHelper
  {
    public CheckinOpenHelper(Context paramContext)
    {
      super("checkins.db", null, 1);
    }
    
    public void onCreate(SQLiteDatabase paramSQLiteDatabase)
    {
      paramSQLiteDatabase.execSQL("CREATE TABLE checkins(id INTEGER PRIMARY KEY, checkinID TEXT, venueName TEXT, dateTime TEXT, latitude TEXT, longitude TEXT)");
      paramSQLiteDatabase.execSQL("CREATE TABLE autocheckin(id INTEGER PRIMARY KEY, dateTime TEXT, latitude TEXT, longitude TEXT)");
    }
    
    public void onUpgrade(SQLiteDatabase paramSQLiteDatabase, int paramInt1, int paramInt2)
    {
      Log.w("Oh snap", "Upgrading");
      paramSQLiteDatabase.execSQL("DROP TABLE IF EXISTS checkins");
      paramSQLiteDatabase.execSQL("DROP TABLE IF EXISTS autocheckin");
      onCreate(paramSQLiteDatabase);
    }
  }
}
