
tags=['keywords', 'Forgotten Realms', 'Medieval Fantasy Setting', 'D&D']

# To join a list of strings into a single string, use the join() method.
# To make the sentence more readable, we can add "and" before the last item in the list.

if len(tags) > 1:
    sentence = '{} and {}'.format(', '.join(tags[:-1]), tags[-1])
else:
    sentence = tags[0]
print(sentence)
