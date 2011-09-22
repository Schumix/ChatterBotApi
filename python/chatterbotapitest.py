from chatterbotapi import ChatterBotFactory, ChatterBotType

factory = ChatterBotFactory()

bot1 = factory.create(ChatterBotType.CLEVERBOT)
bot1session = bot1.create_session()

bot2 = factory.create(ChatterBotType.PANDORABOTS, 'd689f7b8de347251')
bot2session = bot2.create_session()

s = 'Hi'
while (1):
    
    print 'bot1> ' + s
    
    s = bot2session.think(s);
    print 'bot2> ' + s
    
    s = bot1session.think(s);
