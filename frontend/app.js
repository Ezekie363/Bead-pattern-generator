const { createApp, ref, computed, onMounted } = Vue;

createApp({
  setup() {
    // ── State ──────────────────────────────────────────────────
    const palettes = ref([]);
    const selectedPalette = ref('sanbing');

    const presets = [
      { label: '29×29（小方板）', width: 29, height: 29 },
      { label: '48×48（标准板）', width: 48, height: 48 },
      { label: '58×58（大板）',   width: 58, height: 58 },
      { label: '自定义',           width: null, height: null },
    ];
    const selectedPreset = ref('48×48（标准板）');
    const isCustom = ref(false);
    const customWidth = ref(48);
    const customHeight = ref(48);

    const uploadedImage = ref(null);
    const imagePreviewUrl = ref(null);
    const isDragging = ref(false);

    const gridData = ref(null);
    const stats = ref([]);
    const isProcessing = ref(false);

    const toast = ref({ show: false, message: '', type: 'success' });

    // ── Computed ────────────────────────────────────────────────
    const currentWidth = computed(() => {
      if (isCustom.value) return customWidth.value;
      return presets.find(p => p.label === selectedPreset.value)?.width ?? 48;
    });

    const currentHeight = computed(() => {
      if (isCustom.value) return customHeight.value;
      return presets.find(p => p.label === selectedPreset.value)?.height ?? 48;
    });

    const colorMap = computed(() => {
      const map = {};
      stats.value.forEach(s => { map[s.code] = s.hex; });
      return map;
    });

    const gridStyle = computed(() => ({
      display: 'inline-block',
    }));

    // ── Lifecycle ───────────────────────────────────────────────
    onMounted(async () => {
      const res = await fetch('/api/palettes');
      palettes.value = await res.json();
    });

    // ── Methods ─────────────────────────────────────────────────
    function onPresetChange() {
      isCustom.value = selectedPreset.value === '自定义';
    }

    function handleFileSelect(file) {
      if (!file || !file.type.startsWith('image/')) return;
      uploadedImage.value = file;
      if (imagePreviewUrl.value) URL.revokeObjectURL(imagePreviewUrl.value);
      imagePreviewUrl.value = URL.createObjectURL(file);
      gridData.value = null;
      stats.value = [];
    }

    function onFileInput(event) {
      handleFileSelect(event.target.files[0]);
    }

    function onDrop(event) {
      isDragging.value = false;
      handleFileSelect(event.dataTransfer.files[0]);
    }

    async function processImage() {
      if (!uploadedImage.value) return;
      isProcessing.value = true;

      const formData = new FormData();
      formData.append('image', uploadedImage.value);
      formData.append('palette', selectedPalette.value);
      formData.append('width', currentWidth.value);
      formData.append('height', currentHeight.value);

      try {
        const res = await fetch('/api/process', { method: 'POST', body: formData });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || '处理失败');
        gridData.value = data.grid;
        stats.value = data.stats;
        showToast('✅ 图纸生成成功！', 'success');
      } catch (e) {
        showToast(`❌ ${e.message}，请重试`, 'error');
      } finally {
        isProcessing.value = false;
      }
    }

    function showToast(message, type) {
      toast.value = { show: true, message, type };
      setTimeout(() => { toast.value = { ...toast.value, show: false }; }, 2000);
    }

    function getTextColor(hex) {
      if (!hex) return '#000';
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);
      return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.5 ? '#000000' : '#ffffff';
    }

    function exportPng() {
      if (!gridData.value || !stats.value.length) return;

      const cellSize = 14;
      const statsBarH = 50;
      const cols = gridData.value[0].length;
      const rows = gridData.value.length;
      const W = cols * cellSize;
      const H = rows * cellSize + statsBarH;

      const canvas = document.createElement('canvas');
      canvas.width = W;
      canvas.height = H;
      const ctx = canvas.getContext('2d');

      // Draw grid cells
      gridData.value.forEach((row, ri) => {
        row.forEach((code, ci) => {
          const hex = colorMap.value[code] || '#ffffff';
          ctx.fillStyle = hex;
          ctx.fillRect(ci * cellSize, ri * cellSize, cellSize, cellSize);
          ctx.strokeStyle = 'rgba(0,0,0,0.12)';
          ctx.lineWidth = 0.5;
          ctx.strokeRect(ci * cellSize, ri * cellSize, cellSize, cellSize);

          ctx.fillStyle = getTextColor(hex);
          ctx.font = `${cellSize * 0.32}px Arial`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(code, ci * cellSize + cellSize / 2, ri * cellSize + cellSize / 2);
        });
      });

      // Draw stats bar background
      ctx.fillStyle = '#1a1a2e';
      ctx.fillRect(0, rows * cellSize, W, statsBarH);

      // Draw stats items
      ctx.font = '11px Arial';
      const swatchSize = 12;
      const padding = 10;
      let x = padding;
      const y = rows * cellSize + statsBarH / 2;

      stats.value.forEach(s => {
        if (x > W - 60) return;
        ctx.fillStyle = s.hex;
        ctx.fillRect(x, y - swatchSize / 2, swatchSize, swatchSize);
        x += swatchSize + 4;

        const label = `${s.code}(${s.count})`;
        ctx.fillStyle = '#e0e0e0';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, x, y);
        x += ctx.measureText(label).width + 14;
      });

      const link = document.createElement('a');
      link.download = 'bead-pattern.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    }

    return {
      palettes, selectedPalette, presets, selectedPreset,
      isCustom, customWidth, customHeight, currentWidth, currentHeight,
      uploadedImage, imagePreviewUrl, isDragging,
      gridData, stats, colorMap, gridStyle,
      isProcessing, toast,
      onPresetChange, onFileInput, onDrop, processImage, getTextColor, exportPng,
    };
  }
}).mount('#app');
