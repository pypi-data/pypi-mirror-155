# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent

class AchievementCompServer(BaseComponent):
    def GetNodeDetailInfo(self, PlayerID, NodeID):
        # type: (str, str) -> dict
        """
        获取对应玩家的对应节点进度
        """
        pass

    def SetNodeFinish(self, PlayerID, NodeID):
        # type: (str, str) -> bool
        """
        设置对应玩家的对应成就节点完成
        """
        pass

    def AddNodeProgress(self, PlayerID, NodeID, Delta):
        # type: (str, str, int) -> bool
        """
        增加对应玩家的对应成就节点的成就进度
        """
        pass

    def GetChildrenNode(self, NodeID):
        # type: (str) -> List
        """
        获得该成就节点的所有孩子节点
        """
        pass

    def LobbyGetAchievementStorage(self, callback, playerID):
        # type: (function, int) -> None
        """
        获取成就节点的存储的数据。仅联机大厅可用
        """
        pass

    def LobbySetAchievementStorage(self, callback, playerID, NodeID, Delta, GetExtraData=None):
        # type: (function, int, str, int, function) -> None
        """
        添加成就节点的进度。仅联机大厅可用
        """
        pass

