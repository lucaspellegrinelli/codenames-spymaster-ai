# Codenames AI

Code to create an AI to play the game [Codenames](https://codenames.game/) as a Spymaster.

## What does the Spymaster do?

The idea is that the spy master must think of a word (that is not on the game) which connects the most amount of words from his team (blue or red) without connecting to the other team's or black cards.

If he does a good job at it, the Operatives (other players) will have an easier time trying to guess which cards are from their team and which are not.

## Example

This is the game interface:

![codenames interface](https://i.imgur.com/GtfQJsY.png)

If the spymaster was on the red team, saying the word "voador" (flyer) might be a good call to connect the words "drone" and "para-quedas" (parachute) for the operators to choose them. On the other hand, the blue spymaster could make the mistake of saying "animal" trying to connect the words "leão" (lion) and "peru" (turkey) forgetting that the red team has the card "elefante" (elephant) and the operatives won't have any way of knowing which one is correct.

## Running

First you need to generate the word embeddings using the `generateencodings.py` script like

```python generateencodings.py --model models/ptwiki_20180420_100d.txt --words data/words.txt --output embeddings_100d.txt```

That will create the `embeddings_100d.txt` file that contains the embeddings for all words contained in `data/words.txt` using the model `models/ptwiki_20180420_100d.txt`.

Then, with the embeddings file created, we can run the script with

```python main.py --team red --encodings embeddings_100d.txt```