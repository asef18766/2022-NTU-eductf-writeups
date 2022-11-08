void decrypt(char *ct, unsigned int ct_len)
{
  unsigned int i; // [rsp+0h] [rbp-18h]

  for ( i = 0; ; ++i )
  {
    if ( i >= ct_len )
      break;
    ct[i] = i ^ ~ct[i];
  }
}
