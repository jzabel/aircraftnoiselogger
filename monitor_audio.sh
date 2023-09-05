arecord -d 1 --device plughw:CARD=Device,DEV=0 -t wav | sox -t .wav - -n stats 2>&1 | awk '/RMS lev dB/{print $4}'
