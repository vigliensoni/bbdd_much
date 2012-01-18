# <!-- http://bdch.musica.cl/login.php
# http://bdch.musica.cl/track.php?ID=117997


# <form method="post" action="login.php">
#     <table border=0 class=texto>
#         <tr>
#             <td align=left>Nombre : </td>
#             <td><input name="user_name" type=text size=16 maxlength=16 value="" class=boton>
#         </tr>
#         <tr>
#             <td align=left>Contrase&ntilde;a : </td>
#             <td><input name="password" type=password size=16 value=""class=boton ></tr>
#         <tr>
#             <td align=right><input type=submit name="login" value="Entrar" class=boton></td>
#         </tr>
#     </table>
# </form>
#  -->
import requests
from BeautifulSoup import BeautifulSoup
import sys, urllib2, re, os

USER = ''
PASS = ''

URL = 'http://bdch.musica.cl/login.php'

def main():
    # Start a session so we can have persistant cookies
    session = requests.session(config={'verbose': sys.stderr})

    # This is the form data that the page sends when logging in
    login_data = {
    'user_name': USER,
    'password': PASS,
    'login': 'Entrar',
    }

    # Authenticate
    r = session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in
    page = session.get('http://bdch.musica.cl/track.php?ID=117997)') 
    print page
    soup = BeautifulSoup(page.content)
    ventana = soup.find('div', {'class':"ventana"})
    



if __name__ == '__main__':
    main()