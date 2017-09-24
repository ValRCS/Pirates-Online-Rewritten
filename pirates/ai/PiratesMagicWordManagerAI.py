from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from pirates.uberdog.AIMagicWordTrade import AIMagicWordTrade
from pirates.quest.QuestDB import QuestDict

class PiratesMagicWordManagerAI(MagicWordManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        MagicWordManagerAI.__init__(self, air)
        
    def setMagicWord(self, magicWord, avId, zoneId, userSignature): 
        msg = ""
        if magicWord.count("setMoney"):
            args = magicWord.split()
            if len(args) <= 1:
                msg = "MW: Invalid number of arguments! (2 arguments or more are needed)"
                self.setMagicWordResponse(avId, msg)
                return
            av = simbase.air.doId2do.get(avId, None)
            if not av:
                return
            count = int(args[1])
            curGold = av.getInventory().getGoldInPocket()
            # print "Debug: Args being passed to AIMAgicWordTrade:\t%s" % av
            trade = AIMagicWordTrade(av, av.getDoId(), avatarId = av.getDoId())
            if count > curGold:
                trade.giveGoldInPocket(count - curGold)
            else:
                trade.takeGoldInPocket(curGold - count)
            trade.sendTrade()
            msg = "MW: Set Money!"
            
        if msg != "":
            self.setMagicWordResponse(avId, msg)