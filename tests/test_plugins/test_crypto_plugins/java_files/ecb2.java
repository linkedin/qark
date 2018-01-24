class Example{
	public static void main(){
		Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding", "SunJCE");
		Key skeySpec = KeyGenerator.getInstance("AES").generateKey();
		cipher.init(Cipher.ENCRYPT_MODE, skeySpec);
		System.out.println(Arrays.toString(cipher.doFinal(new byte[] { 0, 1, 2, 3 })));
	}
}
