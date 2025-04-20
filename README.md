[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate?hosted_button_id=JF5BEQE3YQGH2)   

![alt text](https://i.imgur.com/DYVm3u6.png)

[Standalone executables](https://github.com/Purfview/whisper-standalone-win/releases) of [OpenAI's Whisper](https://github.com/openai/whisper) & [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) for those who don't want to bother with Python.

**Faster-Whisper** - executables are x86-64 compatible with Windows 7, Linux v5.4, macOS v10.15 and above.   
**Faster-Whisper-XXL** - the last executables are x86-64 compatible with Windows 10, Linux v5.15 and above.       
[**Faster-Whisper-XXL Pro**](https://github.com/Purfview/whisper-standalone-win/discussions/456) - as above. Special non-public version for the donators.           
**Whisper** - executables are x86-64 compatible with Windows 10 and above.   
     
Meant to be used in command-line interface or in programs like:   
[Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit), [Tero Subtitler](https://github.com/URUWorks/TeroSubtitler), [FFAStrans](https://ffastrans.com/wp/), [AviUtl](https://github.com/oov/aviutl_subtitler), [PotPlayer](https://potplayer.daum.net)           
Faster-Whisper is much faster & better than OpenAI's Whisper, and it requires less RAM/VRAM.

## Usage examples:
* `faster-whisper-xxl.exe "D:\videofile.mkv" --language English --model medium --output_dir source`
* `faster-whisper-xxl.exe "D:\Folder" -l en -m turbo --sentence --batch_recursive`
* `faster-whisper-xxl.exe "D:\videofile.mkv" -l ja -m medium --task translate --standard -o source`      
* `faster-whisper-xxl.exe --help`

## Notes:

Executables & libs can be downloaded from `Releases`. [at the right side of this page]    
Don't copy programs to the Windows' folders! [run as Administrator if you did]       
Programs automatically will choose to work on GPU if CUDA is detected.   
For decent transcription use not smaller than `medium` model.   
Guide how to run the command line programs: https://www.youtube.com/watch?v=A3nwRCV-bTU     

## Standalone Whisper info:

Vanilla Whisper, compiled as is - no changes to the original code.   
A reference implementation, stagnant development, atm maybe useful for some tests.
   
## Standalone Faster-Whisper info:

Some defaults are tweaked for movies transcriptions and to make it portable.    
Features various new experimental settings and tweaks.   
Shows the progress bar in the title bar of command-line interface. [or it can be printed with `-pp`]   
By default it looks for models in the same folder, in path like this -> `_models\faster-whisper-medium`.   
Models are downloaded automatically or can be downloaded manually from: [Systran](https://huggingface.co/Systran) & [Purfview](https://huggingface.co/Purfview)        
Deprecated. Use Faster-Whisper-XXL

## Standalone Faster-Whisper-XXL info:

Includes all Standalone Faster-Whisper features + the additional ones, for example:   
Preprocess audio with MDX23 Kim_vocal_v2 vocal extraction model.   
Alternative VAD methods: 'silero_v3', 'silero_v4', 'silero_v5', 'pyannote_v3', 'pyannote_onnx_v3', 'auditok', 'webrtc'.   
[Speaker Diarization](https://github.com/Purfview/whisper-standalone-win/discussions/322).    
Read more about new features in [the Discussions' thread](https://github.com/Purfview/whisper-standalone-win/discussions/231).

## Standalone Faster-Whisper-XXL Pro info:    
    
Special non-public version for the donators.     
Includes some new advanced features, there is the log: [the Discussions' thread](https://github.com/Purfview/whisper-standalone-win/discussions/456).  
       
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=JF5BEQE3YQGH2)


