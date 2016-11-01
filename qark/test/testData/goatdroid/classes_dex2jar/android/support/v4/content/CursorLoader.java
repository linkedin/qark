package android.support.v4.content;

import android.content.ContentResolver;
import android.content.Context;
import android.database.ContentObserver;
import android.database.Cursor;
import android.net.Uri;
import java.io.FileDescriptor;
import java.io.PrintWriter;
import java.util.Arrays;

public class CursorLoader
  extends AsyncTaskLoader<Cursor>
{
  Cursor mCursor;
  final Loader<Cursor>.ForceLoadContentObserver mObserver = new Loader.ForceLoadContentObserver(this);
  String[] mProjection;
  String mSelection;
  String[] mSelectionArgs;
  String mSortOrder;
  Uri mUri;
  
  public CursorLoader(Context paramContext)
  {
    super(paramContext);
  }
  
  public CursorLoader(Context paramContext, Uri paramUri, String[] paramArrayOfString1, String paramString1, String[] paramArrayOfString2, String paramString2)
  {
    super(paramContext);
    this.mUri = paramUri;
    this.mProjection = paramArrayOfString1;
    this.mSelection = paramString1;
    this.mSelectionArgs = paramArrayOfString2;
    this.mSortOrder = paramString2;
  }
  
  public void deliverResult(Cursor paramCursor)
  {
    if (isReset()) {
      if (paramCursor != null) {
        paramCursor.close();
      }
    }
    Cursor localCursor;
    do
    {
      return;
      localCursor = this.mCursor;
      this.mCursor = paramCursor;
      if (isStarted()) {
        super.deliverResult(paramCursor);
      }
    } while ((localCursor == null) || (localCursor == paramCursor) || (localCursor.isClosed()));
    localCursor.close();
  }
  
  public void dump(String paramString, FileDescriptor paramFileDescriptor, PrintWriter paramPrintWriter, String[] paramArrayOfString)
  {
    super.dump(paramString, paramFileDescriptor, paramPrintWriter, paramArrayOfString);
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mUri=");
    paramPrintWriter.println(this.mUri);
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mProjection=");
    paramPrintWriter.println(Arrays.toString(this.mProjection));
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mSelection=");
    paramPrintWriter.println(this.mSelection);
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mSelectionArgs=");
    paramPrintWriter.println(Arrays.toString(this.mSelectionArgs));
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mSortOrder=");
    paramPrintWriter.println(this.mSortOrder);
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mCursor=");
    paramPrintWriter.println(this.mCursor);
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mContentChanged=");
    paramPrintWriter.println(this.mContentChanged);
  }
  
  public String[] getProjection()
  {
    return this.mProjection;
  }
  
  public String getSelection()
  {
    return this.mSelection;
  }
  
  public String[] getSelectionArgs()
  {
    return this.mSelectionArgs;
  }
  
  public String getSortOrder()
  {
    return this.mSortOrder;
  }
  
  public Uri getUri()
  {
    return this.mUri;
  }
  
  public Cursor loadInBackground()
  {
    Cursor localCursor = getContext().getContentResolver().query(this.mUri, this.mProjection, this.mSelection, this.mSelectionArgs, this.mSortOrder);
    if (localCursor != null)
    {
      localCursor.getCount();
      registerContentObserver(localCursor, this.mObserver);
    }
    return localCursor;
  }
  
  public void onCanceled(Cursor paramCursor)
  {
    if ((paramCursor != null) && (!paramCursor.isClosed())) {
      paramCursor.close();
    }
  }
  
  protected void onReset()
  {
    super.onReset();
    onStopLoading();
    if ((this.mCursor != null) && (!this.mCursor.isClosed())) {
      this.mCursor.close();
    }
    this.mCursor = null;
  }
  
  protected void onStartLoading()
  {
    if (this.mCursor != null) {
      deliverResult(this.mCursor);
    }
    if ((takeContentChanged()) || (this.mCursor == null)) {
      forceLoad();
    }
  }
  
  protected void onStopLoading()
  {
    cancelLoad();
  }
  
  void registerContentObserver(Cursor paramCursor, ContentObserver paramContentObserver)
  {
    paramCursor.registerContentObserver(this.mObserver);
  }
  
  public void setProjection(String[] paramArrayOfString)
  {
    this.mProjection = paramArrayOfString;
  }
  
  public void setSelection(String paramString)
  {
    this.mSelection = paramString;
  }
  
  public void setSelectionArgs(String[] paramArrayOfString)
  {
    this.mSelectionArgs = paramArrayOfString;
  }
  
  public void setSortOrder(String paramString)
  {
    this.mSortOrder = paramString;
  }
  
  public void setUri(Uri paramUri)
  {
    this.mUri = paramUri;
  }
}
