import { aa as ordered_colors } from './index.40d901dd.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
