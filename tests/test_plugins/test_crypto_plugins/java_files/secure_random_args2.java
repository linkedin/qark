import java.security.SecureRandom;
import java.math.BigInteger;

class Aoeu{
	public BigInteger generate(){
		SecureRandom random = new SecureRandom();
		Random r = new Random();
		int seed = r.nextInt();
		random.setSeed(seed);
		return new BigInteger(130, random).toString(32);
	}

}
