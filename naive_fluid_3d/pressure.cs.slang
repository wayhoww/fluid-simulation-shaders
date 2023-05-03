import common;

Texture3D<float4> Pressure;
Texture3D<float4> Divergence;

RWTexture3D<float4> OutPressure;

[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;

    float pressure_0 = Pressure[thread_id.xyz + int3( 1, 0, 0)].x;
    float pressure_1 = Pressure[thread_id.xyz + int3(-1, 0, 0)].x;
    float pressure_2 = Pressure[thread_id.xyz + int3(0,  1, 0)].x;
    float pressure_3 = Pressure[thread_id.xyz + int3(0, -1, 0)].x;
    float pressure_4 = Pressure[thread_id.xyz + int3(0, 0,  1)].x;
    float pressure_5 = Pressure[thread_id.xyz + int3(0, 0, -1)].x;

    float divergence = Divergence[thread_id.xyz].x;

    float pressure = ( - CELL_SIZE * CELL_SIZE * divergence + pressure_0 + pressure_1 + pressure_2 + pressure_3 + pressure_4 + pressure_5) / 6;
    OutPressure[thread_id.xyz] = float4(pressure, 0, 0, 0);
}
