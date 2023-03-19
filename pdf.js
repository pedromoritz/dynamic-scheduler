function BoxMullerTransform() {
	const u1 = Math.random();
    const u2 = Math.random();
    const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    const z1 = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);
    return { z0, z1 };
}

export function getNormallyDistributedRandomNumber(arraySize) {
	const stddev = 1
	const mean = Math.round(arraySize / 2);
  	const { z0, _ } = BoxMullerTransform();
    return Math.min(arraySize - 1, Math.max(0, Math.round(z0 * stddev + mean)));
}
