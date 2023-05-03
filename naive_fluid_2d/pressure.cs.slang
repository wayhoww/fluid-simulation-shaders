import common;

Texture2D<float4> Pressure;
Texture2D<float4> Divergence;

RWTexture2D<float4> OutPressure;

[numthreads(16, 16, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    float pressure_1 = Pressure[thread_id.xy + int2( 1, 0)].x;
    float pressure_2 = Pressure[thread_id.xy + int2(-1, 0)].x;
    float pressure_3 = Pressure[thread_id.xy + int2( 0, 1)].x;
    float pressure_4 = Pressure[thread_id.xy + int2( 0,-1)].x;

    float divergence = Divergence[thread_id.xy].x;

    float pressure = ( - CELL_SIZE * CELL_SIZE * divergence + pressure_1 + pressure_2 + pressure_3 + pressure_4) / 4;
    OutPressure[thread_id.xy] = float4(pressure, 0, 0, 0);
}
