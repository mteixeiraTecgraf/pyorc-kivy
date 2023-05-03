

 - Rodar o Kivy OK
    - Docker FAIL
    - WSL Ok
 - Deploy Android
    - Python-for-android https://github.com/kivy/python-for-android
        - ? imagem 
    - Buildozer

 - consegui reusar o docker
 - usando buildozer docker
 - problema em baixar o android-ndk-r25b-linux-x86_64.zip
    - Como mudar parametro? nao existe mais r25b(tem r25c nao x86_64)
    - existe r25b-linux(sem x86_64)
    - foi extraido manualmente na pasta .buildozer/android/platform
     - em android-ndk-r25b
     - buildozer angular... continuou corretamente
 - kivy parece estar se mostrando desnecessario no deploy
 - consegui rodar no emulador o teste inicial(x86)
 - importante verificar android.arch dependendo do device
 - camera - permissoes android.permission.CAMERA,android.permission.WRITE_EXTERNAL_STORAGE
 - 


 - Tarefas
  - Testar kivy em android - OK
  - Testar codigo python em android - OK
  - Testar exemplos mais complexos de android - OK
  - Testar api em android/kivy
  - Testar codigo do pyorc em android
  - Testar integracao app android com serverzip



  - Cartopy
    - geos_c.h: No such file or directory
     - Apos instalar libgeos-dev funcionou
    - Problemas em video
      - Instalado libgstreamer1.0
      - pip install ffpyplayer 
   - Cartopy dando problema ao rodar buildozer para deploy para android
      - /usr/include/limits.h:26:10: fatal error: 'bits/libc-header-start.h' file not found
      - possivel solucao sudo apt-get install gcc-multilib
         -  https://stackoverflow.com/questions/54082459/fatal-error-bits-libc-header-start-h-no-such-file-or-directory-while-compili