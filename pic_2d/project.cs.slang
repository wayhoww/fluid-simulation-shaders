import common;

Texture2D<float> Pressure;
Texture2D<float4> GridDataIn;

RWTexture2D<float4> GridVelocity;
RWTexture2D<float4> GridData;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z) {
        return;
    }

    let pressure_0 = Pressure[thread_id.xy + int2( 1, 0)];
    let pressure_1 = Pressure[thread_id.xy + int2(-1, 0)];
    let pressure_2 = Pressure[thread_id.xy + int2( 0, 1)];
    let pressure_3 = Pressure[thread_id.xy + int2( 0,-1)];

    let gradient = float2(pressure_0 - pressure_1, pressure_2 - pressure_3) * 0.5;
    let velocity = GridVelocity[thread_id.xy].xy - gradient;
    GridVelocity[thread_id.xy] = float4(velocity, 0, 0);

    let last_location = thread_id.xy - velocity * DELTA_TIME / GRID_CELL_SIZE;
    let last_data = GridDataIn.Load(last_location);
    GridData[thread_id.xy] = last_data;
}
