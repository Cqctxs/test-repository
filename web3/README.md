# Brawl: The Heist

**allow a zip of the param folder to be downloaded by the user, but replace the FLAG env variable in Dockerfile with wxmctf{dummy_flag}, server is needed to host the program**

## Description
After getting all of his brawlers to 500 trophies, Eatingfood has found himself in a pickle - there is a Fang on the opposing team every other match and he can no longer play the game!
Luckily, he has a plan - to get enough gems to buy every brawler and hypercharge so he can get back to mindlessly mashing buttons and winning.
Not wanting to wait and earn gems slowly by normal methods, he has resorted to some slightly more unethical means - uploading a virus into the Brawl Stars servers which would allow him to siphon gems from other players.
However, the virus has an unexpected effect: it only allows him to transfer gems to other players.
Can you find a way to get him enough gems so he can get back to mindlessly button mashing?

## Flag
`wxmctf{p4rAm373r_P0lLU7IOn}`

## Solution
The form data is sent to a Flask backend, which then performs some basic checks and sends it to a PHP payment gateway running on an Apache server. However, Flask and PHP running on an Apache server interpret HTTP queries differently - for example, the query
```
amount=5&amount=10
```
would be interpreted as ```amount=5``` (first occurrence) by Flask and ```amount=10``` (last occurrence) by PHP running on an Apache server. As a result, a query such as ```amount=100000&recipient=LostCactus&recipient=Eatingfood&sender=LostCactus``` will pass the Flask checks and reach the PHP payment gateway, transferring $100000 from LostCactus to Eatingfood.
