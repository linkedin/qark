package android.support.v4.app;

import android.util.AndroidRuntimeException;

final class SuperNotCalledException
  extends AndroidRuntimeException
{
  public SuperNotCalledException(String paramString)
  {
    super(paramString);
  }
}
