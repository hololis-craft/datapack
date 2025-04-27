# 進捗を付与
execute as @p[tag=LavaFired,scores={LavaFired=1..,DeathCount=1}] run advancement grant @s from hololis:holomem/lava_acchu
# 復活後はリセット
execute as @p[nbt={Fire:0s},tag=LavaFired] run function hololis:hololis/advancement/lava_acchu/reset