import java.security.SecureRandom;
import java.util.Random;

public final class mfo {
    public static final SecureRandom a;
    private static final Random b;

    static {
        b = new mfp();
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextLong();
        a = secureRandom;
    }
}
