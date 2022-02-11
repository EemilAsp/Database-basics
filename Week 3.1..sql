
SELECT * FROM Matches
INNER JOIN Player ON Matches.FK_playerOne=Player.playerid OR Matches.FK_playerTwo=Player.playerid
GROUP BY FK_playerOne,FK_playerTwo OR FK_playerOne,FK_playerTwo
Having COUNT(*) >1;






