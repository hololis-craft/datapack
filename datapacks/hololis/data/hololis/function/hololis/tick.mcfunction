function hololis:hololis/advancement/lava_acchu/on_tick

# Reset death count
execute as @p[scores={DeathCount=1}] run scoreboard players set @s DeathCount 0