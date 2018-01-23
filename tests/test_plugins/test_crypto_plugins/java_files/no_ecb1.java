class Example{
private static String decrypt_data(String encData)
        throws NoSuchAlgorithmException, NoSuchPaddingException,
        InvalidKeyException, IllegalBlockSizeException, BadPaddingException {
    String key = "bad8deadcafef00d";
    SecretKeySpec skeySpec = new SecretKeySpec(key.getBytes(), "AES");
    Cipher cipher = Cipher.getInstance("AES");

    cipher.init(Cipher.DECRYPT_MODE, skeySpec);

    System.out.println("Base64 decoded: "
            + Base64.decode(encData.getBytes()).length);
    byte[] original = cipher
            .doFinal(Base64.decode(encData.getBytes()));
    return new String(original).trim();
}
}
