from falcor import *

def render_graph_DefaultRenderGraph():
    g = RenderGraph('DefaultRenderGraph')
    loadRenderPassLibrary('DLSSPass.dll')
    loadRenderPassLibrary('AccumulatePass.dll')
    loadRenderPassLibrary('BSDFViewer.dll')
    loadRenderPassLibrary('Antialiasing.dll')
    loadRenderPassLibrary('BlitPass.dll')
    loadRenderPassLibrary('CSM.dll')
    loadRenderPassLibrary('DebugPasses.dll')
    loadRenderPassLibrary('PathTracer.dll')
    loadRenderPassLibrary('DepthPass.dll')
    loadRenderPassLibrary('ErrorMeasurePass.dll')
    loadRenderPassLibrary('SimplePostFX.dll')
    loadRenderPassLibrary('FLIPPass.dll')
    loadRenderPassLibrary('ForwardLightingPass.dll')
    loadRenderPassLibrary('GBuffer.dll')
    loadRenderPassLibrary('WhittedRayTracer.dll')
    loadRenderPassLibrary('ImageLoader.dll')
    loadRenderPassLibrary('MinimalPathTracer.dll')
    loadRenderPassLibrary('ModulateIllumination.dll')
    loadRenderPassLibrary('NRDPass.dll')
    loadRenderPassLibrary('PixelInspectorPass.dll')
    loadRenderPassLibrary('SkyBox.dll')
    loadRenderPassLibrary('RTXDIPass.dll')
    loadRenderPassLibrary('RTXGIPass.dll')
    loadRenderPassLibrary('SceneDebugger.dll')
    loadRenderPassLibrary('ScriptableFullScreenPass.dll')
    loadRenderPassLibrary('SDFEditor.dll')
    loadRenderPassLibrary('SSAO.dll')
    loadRenderPassLibrary('SVGFPass.dll')
    loadRenderPassLibrary('TemporalDelayPass.dll')
    loadRenderPassLibrary('TestPasses.dll')
    loadRenderPassLibrary('ToneMapper.dll')
    loadRenderPassLibrary('Utils.dll')

    SIMULATION_TEXTURE_SIZE = uint3(128, 128, 128)
    NUM_THREADS = SIMULATION_TEXTURE_SIZE
    NUM_PRESSURE_ITERATIONS = 10

    InputPass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'input.cs.slang', 'kResources': [ResourceDesc("Velocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Data", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, False)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(InputPass, 'InputPass')
    InitializePass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'initialize.cs.slang', 'kResources': [ResourceDesc("Velocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Data", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out, ResourceDesc.Format.RGBA32F, False)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(InitializePass, 'InitializePass')
    DecomposePass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'decompose.cs.slang', 'kResources': [ResourceDesc("Pressure", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("InOutVelocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, False)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(DecomposePass, 'DecomposePass')
    

    PressurePasses = []
    for i in range(NUM_PRESSURE_ITERATIONS):
        resources = [ ResourceDesc("Divergence", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), 
                      ResourceDesc("OutPressure", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out if i < 2 else ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, True) ]
        if i != 0:
            resources = [ResourceDesc("Pressure", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False)] + resources

        PressurePass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'pressure.cs.slang', 'kResources': resources, 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
        g.addPass(PressurePass, 'PressurePass' + str(i))
        PressurePasses.append(PressurePass)

    AdvectPass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'advect.cs.slang', 'kResources': [ResourceDesc("Velocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Data", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("OutVelocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out, ResourceDesc.Format.RGBA32F, True), ResourceDesc("OutData", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out, ResourceDesc.Format.RGBA32F, True)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(AdvectPass, 'AdvectPass')
    DivergencePass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'divergence.cs.slang', 'kResources': [ResourceDesc("Velocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("OutDivergence", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_Out, ResourceDesc.Format.RGBA32F, True)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(DivergencePass, 'DivergencePass')
    CopyVelocityPass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'copy.cs.slang', 'kResources': [ResourceDesc("Source", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Dest", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, False)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(CopyVelocityPass, 'CopyVelocityPass')
    CopyDataPass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'copy.cs.slang', 'kResources': [ResourceDesc("Source", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Dest", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.UAV_InOut, ResourceDesc.Format.RGBA32F, False)], 'kThreads': NUM_THREADS, 'kCompute': True, 'kAutoThreads': False})
    g.addPass(CopyDataPass, 'CopyDataPass')
    VisualizationPass = createPass('ScriptableFullScreenPass', {'kShaderPath': 'visualization.ps.slang', 'kResources': [ResourceDesc("Velocity", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Data", ResourceDesc.Type.Texture3D, SIMULATION_TEXTURE_SIZE, False, 0, ResourceDesc.View.SRV, ResourceDesc.Format.RGBA32F, False), ResourceDesc("Target", ResourceDesc.Type.Texture2D, uint3(1, 1, 1), True, 0, ResourceDesc.View.RTV_Out, ResourceDesc.Format.RGBA32F, True)], 'kThreads': NUM_THREADS, 'kCompute': False, 'kAutoThreads': False})
    g.addPass(VisualizationPass, 'VisualizationPass')
    g.addEdge('InitializePass.Velocity', 'InputPass.Velocity')
    g.addEdge('InitializePass.Data', 'InputPass.Data')
    g.addEdge('InputPass.Velocity', 'AdvectPass.Velocity')
    g.addEdge('InputPass.Data', 'AdvectPass.Data')
    g.addEdge('InitializePass.Velocity', 'CopyVelocityPass.Dest')
    g.addEdge('InitializePass.Data', 'CopyDataPass.Dest')
    g.addEdge('AdvectPass.OutData', 'CopyDataPass.Source')
    g.addEdge('AdvectPass.OutVelocity', 'DivergencePass.Velocity')
    g.addEdge('DecomposePass.InOutVelocity', 'CopyVelocityPass.Source')
    g.addEdge('AdvectPass.OutVelocity', 'DecomposePass.InOutVelocity')
    g.addEdge('CopyVelocityPass.Dest', 'VisualizationPass.Velocity')
    g.addEdge('CopyDataPass.Dest', 'VisualizationPass.Data')
    
    for i, _ in enumerate(PressurePasses):
        g.addEdge('DivergencePass.OutDivergence', 'PressurePass%s.Divergence' % i)

        if i == len(PressurePasses) - 1:
            g.addEdge('PressurePass%s.OutPressure' % i, 'DecomposePass.Pressure')
        else:
            g.addEdge('PressurePass%s.OutPressure' % i, 'PressurePass%s.Pressure' % (i + 1))

        if i < len(PressurePasses) - 2:
            g.addEdge('PressurePass%s.OutPressure' % i, 'PressurePass%s.OutPressure' % (i + 2))

    g.markOutput('VisualizationPass.Target')
    return g

DefaultRenderGraph = render_graph_DefaultRenderGraph()
try: m.addGraph(DefaultRenderGraph)
except NameError: None
