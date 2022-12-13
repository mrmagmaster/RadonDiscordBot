while true
do
BINDIR=$(dirname "$(readlink -fn "$0")")
cd "$BINDIR"
python3 a.py
echo "A bot újraindul!" 
done
