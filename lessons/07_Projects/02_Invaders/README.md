# League Invaders

Here are the general rules for the classic arcade game **Space Invaders**:

![examples](https://i.ytimg.com/vi/-QaA3ElrOAE/maxresdefault.jpg)

## Objective

The goal of **Space Invaders** is to defend Earth from waves of descending alien invaders by shooting them with your laser cannon while avoiding their attacks. You win by eliminating all invaders before they reach the bottom of the screen.

## Gameplay

1. **Player's Ship (Laser Cannon)**: 
   - The player controls a laser cannon, which moves horizontally along the bottom of the screen. 
   - The cannon can shoot upwards to destroy the approaching alien invaders.
   - The player can only fire one shot at a time, and must wait until the shot has hit an alien or gone off-screen before firing again.
   - they also have an ability to shoot a "mega shot" which is a bullet that grows larger and larger after being shoot. it has a cooldown of 10 and uses a diffrent button

2. **Alien Invaders**: 
   - The aliens are arranged in rows and columns at the top of the screen, slowly moving from side to side while gradually descending toward the player.
   - As the invaders move, they fire projectiles down toward the player’s ship.
   - If an alien reaches the bottom of the screen (the ground), the game is over.
   - The invaders' speed increases as more of them are destroyed, making it harder to hit them and avoid their attacks as the game progresses.

3. **Shields**:
   - There are a few stationary shields (bunkers) positioned between the player and the alien invaders.
   - These shields provide cover from the invaders’ projectiles and can block incoming attacks.
   - However, both the player's shots and the aliens' projectiles will gradually destroy parts of the shields, reducing their effectiveness over time.

4. **UFO (Mystery Ship)**: 
   - Occasionally, a UFO (also called a "mystery ship") appears at the top of the screen, moving across horizontally.
   - Shooting the UFO grants the player extra points, depending on when it is hit.

### Rules

1. **Move and Shoot**:
   - The player can move the laser cannon left or right and shoot upwards to destroy the alien invaders.
   - Only one shot can be fired at a time, so timing and accuracy are important.

2. **Defeating Invaders**:
   - The player must shoot all the alien invaders on the screen to clear the level.
   - As invaders are destroyed, the remaining ones move faster, making them harder to hit.
   - Once all invaders are destroyed, a new wave of invaders appears at the top, with the game becoming progressively harder.

3. **Avoid Being Hit**:
   - The player must avoid being hit by the aliens' projectiles.
   - If the player's laser cannon is hit, they lose a life. The game typically starts with 3 lives, and the game ends when all lives are lost.

4. **Prevent Invaders from Reaching the Bottom**:
   - If an alien reaches the bottom of the screen, the game ends immediately, regardless of how many lives the player has left.
   
5. **Scoring**:
   - Points are awarded for each alien destroyed, with different point values for each row of aliens (higher rows are worth more points).
   - The UFO grants additional bonus points when shot, with the points for the UFO often varying.

## Winning & Losing

- **Winning**: There is no final "win" in **Space Invaders**—the game continues indefinitely as the player clears each wave of invaders. The player's goal is to score as many points as possible and survive for as long as they can.
- **Losing**: The game ends when:
   - The player loses all their lives.
   - An invader reaches the bottom of the screen.

## Progressive Difficulty

- **Speed**: As invaders are destroyed, the remaining aliens move faster, making it harder to shoot them and avoid their attacks.
- **Level Progression**: With each new wave, the invaders start closer to the bottom of the screen, making it more difficult for the player to keep them from reaching the ground.

## Development

### 1 Background and player

Create a window that is the same size as the background, then add a player that can
can move left and right. When the space bar is pressed, make the player shoot a
bullet. Limit the number of bullets on the screen to 3. 

Your bullets should be added to a group, and when the bullet goes off the screen,
it should be removed from the group, using the `kill()` method.


### 2 Add a grid of enemies

Create a grid of enemies. All of the enemies should be sprites, and should be
added to an enemies group. 

Make the enemies move to the left and the right. Move the enemies by iterating
through their group, changing the x position of all enemies by a small amount.
While iterating, check that any enemies has hit the left or right side of the
screen, and if so, move all enemies down and change their direction.

### 3 Add collision detection

Check for collisions: 

* Between the enemies group and the bullets group. If a collision is detected,
  remove the enemy and the bullet from their respective groups.
* Between the enemies group and the player. If a collision is detected, end the
  game or decrement s life. 


### 4 Final Touches. 

* Add a scoring system.
* Add a Start Game and a Game Over screen.

