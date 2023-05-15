def indefinite_article(noun):
    vowel_sound_starts = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    if noun.startswith(vowel_sound_starts):
        return f'an {noun}'
    else:
        return f'a {noun}'
