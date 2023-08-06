import { aa as ordered_colors } from './index.f6fa633d.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
