package org.owasp.goatdroid.fourgoats.db;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteStatement;
import android.util.Log;
import java.util.HashMap;

public class UserInfoDBHelper
{
  private static final String DATABASE_NAME = "userinfo.db";
  private static final int DATABASE_VERSION = 1;
  private static final String DELETE_INFO = "delete from info";
  private static final String INSERT_INFO = "insert into info (sessionToken, userName, isPublic, autoCheckin, isAdmin) values (?,?,?,?,?)";
  private static final String TABLE_NAME = "info";
  private static final String UPDATE_PREFERENCES = "update info set isPublic = ?, autoCheckin = ? where id = 1";
  private Context context;
  private SQLiteDatabase db;
  private SQLiteStatement deleteStmt;
  private SQLiteStatement insertStmt;
  private SQLiteStatement updateStmt;
  
  public UserInfoDBHelper(Context paramContext)
  {
    this.context = paramContext;
    this.db = new UserInfoOpenHelper(this.context).getWritableDatabase();
    this.insertStmt = this.db.compileStatement("insert into info (sessionToken, userName, isPublic, autoCheckin, isAdmin) values (?,?,?,?,?)");
    this.updateStmt = this.db.compileStatement("update info set isPublic = ?, autoCheckin = ? where id = 1");
    this.deleteStmt = this.db.compileStatement("delete from info");
  }
  
  public void close()
  {
    this.db.close();
  }
  
  public void deleteInfo()
  {
    this.deleteStmt.executeInsert();
  }
  
  public boolean getIsAdmin()
  {
    Cursor localCursor = this.db.query("info", new String[] { "isAdmin" }, null, null, null, null, null);
    if (localCursor.moveToFirst()) {
      return localCursor.getString(0).equals("true");
    }
    return false;
  }
  
  public HashMap<String, String> getPreferences()
  {
    HashMap localHashMap = new HashMap();
    Cursor localCursor = this.db.query("info", new String[] { "isPublic", "autoCheckin" }, null, null, null, null, null);
    if (localCursor.moveToFirst())
    {
      localHashMap.put("isPublic", localCursor.getString(0));
      localHashMap.put("autoCheckin", localCursor.getString(1));
    }
    return localHashMap;
  }
  
  public String getSessionToken()
  {
    Cursor localCursor = this.db.query("info", new String[] { "sessionToken" }, null, null, null, null, null);
    if (localCursor.moveToFirst()) {
      return localCursor.getString(0);
    }
    return "";
  }
  
  public String getUserName()
  {
    Cursor localCursor = this.db.query("info", new String[] { "userName" }, null, null, null, null, null);
    if (localCursor.moveToFirst()) {
      return localCursor.getString(0);
    }
    return "";
  }
  
  public void insertSettings(HashMap<String, String> paramHashMap)
  {
    this.insertStmt.bindString(1, (String)paramHashMap.get("sessionToken"));
    this.insertStmt.bindString(2, (String)paramHashMap.get("userName"));
    this.insertStmt.bindString(3, (String)paramHashMap.get("isPublic"));
    this.insertStmt.bindString(4, (String)paramHashMap.get("autoCheckin"));
    this.insertStmt.bindString(5, (String)paramHashMap.get("isAdmin"));
    this.insertStmt.executeInsert();
  }
  
  public void updatePreferences(String paramString1, String paramString2)
  {
    this.updateStmt.bindString(1, paramString1);
    this.updateStmt.bindString(2, paramString2);
    this.updateStmt.executeInsert();
  }
  
  private class UserInfoOpenHelper
    extends SQLiteOpenHelper
  {
    public UserInfoOpenHelper(Context paramContext)
    {
      super("userinfo.db", null, 1);
    }
    
    public void onCreate(SQLiteDatabase paramSQLiteDatabase)
    {
      try
      {
        paramSQLiteDatabase.execSQL("CREATE TABLE info(id INTEGER PRIMARY KEY, sessionToken TEXT, userName TEXT, isPublic INT, autoCheckin INT, isAdmin INT)");
        return;
      }
      catch (RuntimeException localRuntimeException) {}
    }
    
    public void onUpgrade(SQLiteDatabase paramSQLiteDatabase, int paramInt1, int paramInt2)
    {
      Log.w("Oh snap", "Upgrading");
      paramSQLiteDatabase.execSQL("DROP TABLE IF EXISTS info");
      onCreate(paramSQLiteDatabase);
    }
  }
}
