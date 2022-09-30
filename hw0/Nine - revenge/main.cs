using System;
using System.Text;
class MainClass {
	public static void Main (string[] gg) {
byte[] array = Convert.FromBase64String("LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6".Substring(1));
	for (int i = 0; i < array.Length; i++)
	{
		array[i] ^= 135;
	}
		System.Console.WriteLine(Encoding.UTF8.GetString(array));
	}
}