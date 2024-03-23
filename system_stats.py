from psutil import cpu_percent, virtual_memory, disk_usage
import subprocess


def get_system_stat():
    # nvidia-smi --help-query-gpu
    result = subprocess.run([
        "nvidia-smi",
        "--query-gpu=utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu",
        "--format=csv,noheader,nounits"], 
        stdout=subprocess.PIPE).stdout.decode()

    result = [float(i.strip()) for i in result.split(",")]
    utilization_gpu, memory_used, memory_total, power_draw, temperature_gpu = result
    vram_percent = memory_used / memory_total * 100
    
    return dict(
        cpu=cpu_percent(),
        disk=disk_usage("/").percent,
        ram=virtual_memory().percent,
        vram=vram_percent,
        gpu=utilization_gpu,
        power=power_draw,
        temp=temperature_gpu
        )


if __name__ == "__main__":
    stats = get_system_stat()
    print(f"CPU: {stats['cpu']}% \nDisk: {stats['disk']}% \nRAM: {stats['ram']}% \nVRAM: {round(stats['vram'],2)}%")
    print(f"GPU: {stats['gpu']}% \nPower: {stats['power']}W \nTemp: {stats['temp']}°C")
