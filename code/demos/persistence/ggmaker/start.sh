#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./start.sh <title>"
    exit 1
fi

TITLE="$1"

if [ ! -d "$TITLE/start" ]; then
    echo "Error: game '$TITLE' not found. Run 'make' first."
    exit 1
fi

TEMP_RC=$(mktemp)

cat > "$TEMP_RC" << EOF

show_img() {
    printf '\033[H'
    kitten icat "\$1" 2>/dev/null || img2sixel "\$1" 2>/dev/null
}

fade_in() {
    local img="\$1"
    local size=\$(magick identify -format "%wx%h" "\$img")
    for pct in 0 33 66 100; do
        local inv=\$((100-pct))
        magick -size "\$size" xc:white "\$img" -compose blend -define compose:args="\$pct,\$inv" -composite /tmp/gg_frame.jpg
        show_img /tmp/gg_frame.jpg
        sleep 0.5
    done
    rm -f /tmp/gg_frame.jpg
}

cd() {
    builtin cd "\$@"
    clear
    if [ -f .scene.jpg ]; then fade_in .scene.jpg; fi
    echo
    echo
    if [ -f .description ]; then
        cat .description | python3 -c 'import sys,time;[print(c,end="",flush=True) or time.sleep(0.03) for c in sys.stdin.read()]'
    fi
    read
    echo
    echo "---"
    ls | cat
    echo
}
alias q=exit
cd $TITLE/start
export PS1='(galgame) '
EOF

bash --rcfile "$TEMP_RC"
rm "$TEMP_RC"
