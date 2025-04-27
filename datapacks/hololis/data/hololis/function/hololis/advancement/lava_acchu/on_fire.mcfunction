advancement revoke @s from hololis:hololis_internal/lava_acchu_fire
# インベントリをカウント
execute store result score @s Temp run clear @s * 0
scoreboard players set @s Temp2 0
# アイテムがあったら
execute if score @s Temp > @s Temp2 run scoreboard players add @s LavaFired 1
tag @s add LavaFired