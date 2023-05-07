import typing

# math
class uint2:
    def __init__(self, x: int, y: int) -> None: ...

class uint3:
    def __init__(self, x: int, y: int, z: int) -> None: ...


# Scriptable
class ResourceDesc:
    def __init__(self, identifier: str, type: ResourceDesc.Type, size: uint3, autoSized: bool, targetSlot: int, view: ResourceDesc.View, format: ResourceDesc.Format, clear: bool, optional: bool=True) -> None: ...

    @property
    def identifier(self) -> str: ...

    @property
    def type(self) -> ResourceDesc.Type: ...

    @property
    def size(self) -> uint3: ...

    @property
    def autoSized(self) -> bool: ...

    @property
    def targetSlot(self) -> int: ...

    @property
    def view(self) -> ResourceDesc.View: ...

    @property
    def format(self) -> ResourceDesc.Format: ...

    @property
    def clear(self) -> bool: ...

    @property
    def optional(self) -> bool: ...

    def clone(self) -> ResourceDesc: ...

    class Type:
        Texture1D = 0
        Texture2D = 1
        Texture3D = 2
        Texture2DArray = 3
        TextureCube = 4
        RawBuffer = 5

    class View:
        RTV_Out = 0
        RTV_InOut = 1
        UAV_Out = 2
        UAV_InOut = 3
        SRV = 4

    class Format:
        Auto = 0
        Unknown = 1
        RGBA32F = 2
        RGBA32U = 3
        RGBA32I = 4
        RGBA8Unorm = 5
        R32F = 6
        R32U = 7
        R32I = 8


# graph & pass


class RenderPass:
    def __init__(self) -> None: ...


class ScriptableFullScreenPass(RenderPass):    
    @property
    def shaderPath(self) -> str: ...

    @property
    def resources(self) -> typing.List[ResourceDesc]: ...

    @property
    def threads(self) -> uint3: ...

    @property
    def compute(self) -> bool: ...

    @property
    def autoThreads(self) -> bool: ...


class RenderGraph:
    def __init__(self) -> None: ...
    def addPass(self, passObj: RenderPass, name: str) -> None: ...
    def addEdge(self, src: str, dst: str) -> None: ...
    def markOutput(self, name: str) -> None: ...


class FalcorModule:
    def addGraph(self, name: str, graph: RenderGraph) -> None: ...


m: FalcorModule


def loadRenderPassLibrary(path: str) -> None: ...


def createPass(name: str, args: typing.Dict[str, typing.Any]) -> RenderPass: ...
