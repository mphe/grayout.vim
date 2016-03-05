#ifndef FOOBAR
#   define FOOBAR
#else
#   define ASDF
#endif

#ifdef FOOBAR
#   ifdef ASDF
#       define THIS_SHOULDNT_HAPPEN
#   endif
#   define ASDF
#   if !defined(ASDF)
#       define HJKL
#   else
#       define TRUTH 42
#   endif
#endif

int main(int argc, char *argv[])
{
    return 0;
}
