# Changelog

## v0.014 2024/05/27

- Feature: Added option to search and choose which account to download media from. This should allow users to more quickly download/update their offline cache for a specific account when compared to letting the program complete its longer loop through all followed accounts.
- Feature: Added a main menu with options for users. This means it requires a bit more interaction than before, but lets users have a bit more control.

## v0.013 2024/05/12

- Bug fix: Rewrote get_attachment_data() to handle accounts that host data off Baraag, but the given URL is not a direct link. This requires the file to be fetched temporarily so the function can assign it a proper name and extension. It was literally one attachment out of thousands across a hundred accounts, but better have this properly handled than not.

## v0.012 2024/05/11

- Bug fix: Rewrote get_attachment_data() to handle accounts that don't host media on Baraag, but only use it as a proxy; Current testing shows it now works for accounts that actually host media remotely on misskey.

-Bug fix: Fixed Keyboard interrupt not working properly.

## v0.011 2024/05/11

- Bug fix: Rewrote get_following() so it won't return an empty result should a user follow less than 40 accounts on Baraag;

- This has the added bonus of making the tool more compatible with Pawoo during testing.


## v0.01 2024/05/10

- Initial Release