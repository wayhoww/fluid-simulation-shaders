from falcor import *
from copy import deepcopy

def makePIC2D():
    g = RenderGraph('PIC2D')

    loadRenderPassLibrary('ScriptableFullScreenPass.dll')

    GRID_SIZE = 512
    PARTICLE_PER_GRID = 9
    PARTICLE_COUNT = (GRID_SIZE - 1) * (GRID_SIZE - 1) * PARTICLE_PER_GRID
    PRESSURE_ITERATIONS = 128

    # 一些本应该放在 C++ 层的变量。直接在 shader 里定义了。
    StaticBufferDesc_InOut = ResourceDesc(
        identifier='Static',
        type=ResourceDesc.Type.RawBuffer,
        size=uint3(1 << 16, 1, 1),
        autoSized=False,
        format=ResourceDesc.Format.Unknown,
        clear=False,
        view=ResourceDesc.View.UAV_InOut
    )
    StaticBufferDesc_Out = StaticBufferDesc_InOut.clone()
    StaticBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    StaticBufferDesc_In = StaticBufferDesc_InOut.clone()
    StaticBufferDesc_In.view = ResourceDesc.View.SRV

    ParticleBufferDesc_InOut = ResourceDesc(
        identifier='Particle',
        type=ResourceDesc.Type.RawBuffer,
        size=uint3(PARTICLE_COUNT * 4 * 4, 1, 1),
        autoSized=False,
        format=ResourceDesc.Format.Unknown,
        clear=False,
        view=ResourceDesc.View.UAV_InOut
    )
    ParticleBufferDesc_In = ParticleBufferDesc_InOut.clone()
    ParticleBufferDesc_In.view = ResourceDesc.View.SRV
    ParticleBufferDesc_Out = ParticleBufferDesc_InOut.clone()
    ParticleBufferDesc_Out.view = ResourceDesc.View.UAV_Out

    GridVelocityFixedBufferDesc_InOut = ResourceDesc(
        identifier='GridVelocityFixed',
        type=ResourceDesc.Type.Texture2DArray,
        size=uint3(GRID_SIZE, GRID_SIZE, 3),
        autoSized=False,
        format=ResourceDesc.Format.R32I,
        view=ResourceDesc.View.UAV_InOut,
        optional=False
    )
    GridVelocityFixedBufferDesc_Out = GridVelocityFixedBufferDesc_InOut.clone()
    GridVelocityFixedBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    GridVelocityFixedBufferDesc_Out.clear = True
    GridVelocityFixedBufferDesc_In = GridVelocityFixedBufferDesc_InOut.clone()
    GridVelocityFixedBufferDesc_In.view = ResourceDesc.View.SRV

    GridVelocityBufferDesc_InOut = ResourceDesc(
        identifier='GridVelocity',
        type=ResourceDesc.Type.Texture2D,
        size=uint3(GRID_SIZE, GRID_SIZE, 1),
        autoSized=False,
        format=ResourceDesc.Format.RGBA32F,
        clear=False,
        view=ResourceDesc.View.UAV_InOut,
        optional=False
    )
    GridVelocityBufferDesc_Out = GridVelocityBufferDesc_InOut.clone()
    GridVelocityBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    GridVelocityBufferDesc_In = GridVelocityBufferDesc_InOut.clone()
    GridVelocityBufferDesc_In.view = ResourceDesc.View.SRV

    GridDataBufferDesc_InOut = ResourceDesc(
        identifier='GridData',
        type=ResourceDesc.Type.Texture2D,
        size=uint3(GRID_SIZE, GRID_SIZE, 1),
        autoSized=False,
        format=ResourceDesc.Format.RGBA32F,
        clear=False,
        view=ResourceDesc.View.UAV_InOut,
    )
    GridDataBufferDesc_Out = GridDataBufferDesc_InOut.clone()
    GridDataBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    GridDataBufferDesc_In = GridDataBufferDesc_InOut.clone()
    GridDataBufferDesc_In.view = ResourceDesc.View.SRV
    GridDataBufferDesc_In.identifier = 'GridDataIn'

    DivergenceBufferDesc_InOut = ResourceDesc(
        identifier='Divergence',
        type=ResourceDesc.Type.Texture2D,
        size=uint3(GRID_SIZE, GRID_SIZE, 1),
        autoSized=False,
        format=ResourceDesc.Format.R32F,
        clear=True,
        view=ResourceDesc.View.UAV_InOut,
    )
    DivergenceBufferDesc_Out = DivergenceBufferDesc_InOut.clone()
    DivergenceBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    DivergenceBufferDesc_In = DivergenceBufferDesc_InOut.clone()
    DivergenceBufferDesc_In.view = ResourceDesc.View.SRV

    PressureBufferDesc_InOut = ResourceDesc(
        identifier='Pressure',
        type=ResourceDesc.Type.Texture2D,
        size=uint3(GRID_SIZE, GRID_SIZE, 1),
        autoSized=False,
        format=ResourceDesc.Format.R32F,
        clear=True,
        view=ResourceDesc.View.UAV_InOut,
    )
    PressureBufferDesc_Out = PressureBufferDesc_InOut.clone()
    PressureBufferDesc_Out.view = ResourceDesc.View.UAV_Out
    PressureBufferDesc_In = PressureBufferDesc_InOut.clone()
    PressureBufferDesc_In.identifier = 'PressureIn'
    PressureBufferDesc_In.view = ResourceDesc.View.SRV
    PressureBufferDesc_In.clear = False

    MeaninglessSinkTargetDesc_Out = ResourceDesc(
        identifier='Target',
        type=ResourceDesc.Type.Texture2D,
        size=uint3(1, 1, 1),
        autoSized=False,
        format=ResourceDesc.Format.RGBA8Unorm,
        clear=True,
        view=ResourceDesc.View.RTV_Out,
    )

    InitializePass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'initialize.cs.slang',
            'kResources': [ StaticBufferDesc_Out ],
            'kThreads': uint3(1, 1, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    SpawnParticlePass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'spawn_particle.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, ParticleBufferDesc_Out, GridDataBufferDesc_Out ],
            'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    AdvectPass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'advect.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, ParticleBufferDesc_InOut, GridVelocityFixedBufferDesc_Out ],
            'kThreads': uint3(PARTICLE_COUNT, 1, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    GridVelocityPass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'grid_velocity.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, GridVelocityFixedBufferDesc_In, GridVelocityBufferDesc_Out ],
            'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    DivergencePass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'divergence.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, GridVelocityBufferDesc_In, DivergenceBufferDesc_Out ],
            'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    PressurePasses = []
    for i in range(0, PRESSURE_ITERATIONS):
        if i == 0:
            resources = [ StaticBufferDesc_InOut, DivergenceBufferDesc_In, PressureBufferDesc_Out ]
        elif i == 1:
            resources = [ StaticBufferDesc_InOut, DivergenceBufferDesc_In, PressureBufferDesc_In, PressureBufferDesc_Out ]
        else:
            resources = [ StaticBufferDesc_InOut, DivergenceBufferDesc_In, PressureBufferDesc_In, PressureBufferDesc_InOut ]

        PressurePasses.append(
            createPass(
                'ScriptableFullScreenPass',
                {
                    'kShaderPath': 'pressure.cs.slang',
                    'kResources': resources,
                    'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
                    'kCompute': True,
                    'kAutoThreads': False
                }
            )
        )

    PressureBufferDesc_In_Project = PressureBufferDesc_In.clone()
    PressureBufferDesc_In_Project.identifier = 'Pressure'
    ProjectPass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'project.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, GridVelocityBufferDesc_InOut, PressureBufferDesc_In_Project, GridDataBufferDesc_In, GridDataBufferDesc_Out ],
            'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    # use blit pass later ?
    CopyGridDataPass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'copy_grid_data.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, GridDataBufferDesc_In, GridDataBufferDesc_InOut ],
            'kThreads': uint3(GRID_SIZE, GRID_SIZE, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    ResampePass = createPass(
        'ScriptableFullScreenPass',
        {
            'kShaderPath': 'resample.cs.slang',
            'kResources': [ StaticBufferDesc_InOut, ParticleBufferDesc_InOut, GridVelocityBufferDesc_In ],
            'kThreads': uint3(PARTICLE_COUNT, 1, 1),
            'kCompute': True,
            'kAutoThreads': False
        }
    )

    SinkPass = createPass(
        'ScriptableFullScreenPass', 
        {
            'kShaderPath': '', 
            'kResources': [ StaticBufferDesc_In, ParticleBufferDesc_In, GridDataBufferDesc_In, MeaninglessSinkTargetDesc_Out ], 
            'kCompute': False,
        }
    )

    g.addPass(InitializePass, 'InitializePass')
    g.addPass(SpawnParticlePass, 'SpawnParticlePass')
    g.addPass(AdvectPass, 'AdvectPass')
    g.addPass(GridVelocityPass, 'GridVelocityPass')
    g.addPass(DivergencePass, 'DivergencePass')
    for i, pressure_pass in enumerate(PressurePasses):
        g.addPass(pressure_pass, 'PressurePass_' + str(i))
    g.addPass(ProjectPass, 'ProjectPass')
    g.addPass(CopyGridDataPass, 'CopyGridDataPass')
    g.addPass(ResampePass, 'ResampePass')
    g.addPass(SinkPass, 'SinkPass')
    
    # Initialize
    g.addEdge('InitializePass.Static', 'AdvectPass.Static')

    # SpawnParticle -> Advect
    g.addEdge('InitializePass.Static', 'SpawnParticlePass.Static')
    g.addEdge('SpawnParticlePass.Particle', 'AdvectPass.Particle')

    # Advect -> GridVelocity
    g.addEdge('InitializePass.Static', 'GridVelocityPass.Static')
    g.addEdge('AdvectPass.GridVelocityFixed', 'GridVelocityPass.GridVelocityFixed')

    # GridVelocity -> Divergence
    g.addEdge('InitializePass.Static', 'DivergencePass.Static')
    g.addEdge('GridVelocityPass.GridVelocity', 'DivergencePass.GridVelocity')

    # Pressure
    for i, pressure_pass in enumerate(PressurePasses):
        g.addEdge('InitializePass.Static', 'PressurePass_' + str(i) + '.Static')
        if i == 0:
            g.addEdge('DivergencePass.Divergence', 'PressurePass_' + str(i) + '.Divergence')
        elif i == 1:
            g.addEdge('DivergencePass.Divergence', 'PressurePass_' + str(i) + '.Divergence')
            g.addEdge('PressurePass_' + str(i - 1) + '.Pressure', 'PressurePass_' + str(i) + '.PressureIn')
        else:
            g.addEdge('DivergencePass.Divergence', 'PressurePass_' + str(i) + '.Divergence')
            g.addEdge('PressurePass_' + str(i - 1) + '.Pressure', 'PressurePass_' + str(i) + '.PressureIn')
            g.addEdge('PressurePass_' + str(i - 2) + '.Pressure', 'PressurePass_' + str(i) + '.Pressure') # reuse textures

    # Project
    g.addEdge('InitializePass.Static', 'ProjectPass.Static')
    g.addEdge('GridVelocityPass.GridVelocity', 'ProjectPass.GridVelocity')
    g.addEdge('PressurePass_' + str(PRESSURE_ITERATIONS - 1) + '.Pressure', 'ProjectPass.Pressure')
    g.addEdge('SpawnParticlePass.GridData', 'ProjectPass.GridDataIn')

    # CopyGridData
    g.addEdge('InitializePass.Static', 'CopyGridDataPass.Static')
    g.addEdge('ProjectPass.GridData', 'CopyGridDataPass.GridDataIn')
    g.addEdge('SpawnParticlePass.GridData', 'CopyGridDataPass.GridData')

    # Resample
    g.addEdge('InitializePass.Static', 'ResampePass.Static')
    g.addEdge('AdvectPass.Particle', 'ResampePass.Particle')
    g.addEdge('ProjectPass.GridVelocity', 'ResampePass.GridVelocity')

    # Sink
    g.addEdge('InitializePass.Static', 'SinkPass.Static')
    g.addEdge('ResampePass.Particle', 'SinkPass.Particle')
    g.addEdge('CopyGridDataPass.GridData', 'SinkPass.GridDataIn')

    # out
    g.markOutput('CopyGridDataPass.GridData')
    g.markOutput('ProjectPass.GridVelocity')
    g.markOutput('SinkPass.Target')
    return g

PIC_2D = makePIC2D()
try: m.addGraph(PIC_2D)
except NameError: None
