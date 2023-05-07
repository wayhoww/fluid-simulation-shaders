import common;

Texture2D<float> PressureIn;
Texture2D<float> Divergence;

RWTexture2D<float> Pressure;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z) {
        return;
    }

    let pressure_1 = PressureIn[thread_id.xy + int2(1, 0)];
    let pressure_2 = PressureIn[thread_id.xy + int2(-1, 0)];
    let pressure_3 = PressureIn[thread_id.xy + int2(0, 1)];
    let pressure_4 = PressureIn[thread_id.xy + int2( 0,-1)];

    float divergence = Divergence[thread_id.xy].x;

    float pressure = (-GRID_CELL_SIZE * GRID_CELL_SIZE * divergence + pressure_1 + pressure_2 + pressure_3 + pressure_4) / 4;
    Pressure[thread_id.xy] = pressure;
}
