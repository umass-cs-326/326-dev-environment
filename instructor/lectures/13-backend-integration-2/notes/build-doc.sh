docker run --rm -u "$(id -u):$(id -g)" -v "$(pwd)":/data minlag/mermaid-cli -i 12-backend-integration-1.md -o index.md

docker run --rm \
  --volume "$(pwd):/data" \
  --user "$(id -u):$(id -g)" \
  pandoc/core index.md \
  --standalone \
  --css=assets/pandoc.css \
  -o index.html

rm index.md

OUTDIR="$CLASS_326_F25_DIR_WEBSITE/lectures/12-backend-integration-1"

cp -r assets "$OUTDIR"
mv ./*.svg "$OUTDIR"
mv index.html "$OUTDIR"

echo "Copied to $CLASS_326_F25_DIR_WEBSITE/lectures/12-backend-integration-1"

echo "Publishing..."
if [ -d "$CLASS_326_F25_DIR_WEBSITE" ]; then
  cd "$CLASS_326_F25_DIR_WEBSITE" || {
    echo "Could not cd into $CLASS_326_F25_DIR_WEBSITE. Exiting." >&2
    exit 1
  }
  echo "Publishing to $CLASS_326_F25_DIR_WEBSITE"
  git add .
  git commit -am 'Update Lecture 12'
  git push
else
  echo "$CLASS_326_F25_DIR_WEBSITE does not exist. Cannot publish."
  exit 1
fi

echo "Done."
