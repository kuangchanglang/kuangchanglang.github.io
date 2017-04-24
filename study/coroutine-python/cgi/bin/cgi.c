#include <stdio.h>
#include <stdlib.h>
 
int main(void)
{
    int count = 0;
    printf("Content-type: text/html\r\n"
        "\r\n"
        "<title>CGI Hello!</title>"
 
        "<h1>I'm CGI programed in C!</h1>"
        "Request number %d running on host <i>%s</i>\n",
        ++count, getenv("SERVER_NAME"));
    return 0;
}
