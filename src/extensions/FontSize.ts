import { Mark, mergeAttributes } from '@tiptap/core';
import type { CommandProps, RawCommands } from '@tiptap/core';

export interface FontSizeOptions {
  types: string[];
}

const FontSize = Mark.create<FontSizeOptions>({
  name: 'fontSize',

  addOptions() {
    return {
      types: ['textStyle'],
    };
  },

  addAttributes() {
    return {
      fontSize: {
        default: null,
        parseHTML: (element: HTMLElement) => element.style.fontSize || null,
        renderHTML: (attributes: any) => {
          if (!attributes.fontSize) {
            return {};
          }
          return {
            style: `font-size: ${attributes.fontSize}`,
          };
        },
      },
    };
  },

  parseHTML() {
    return [
      {
        style: 'font-size',
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return ['span', mergeAttributes(HTMLAttributes), 0];
  },

  addCommands() {
    return {
      setFontSize:
        (size: string) =>
        function (this: any): boolean {
          return this.chain().setMark('fontSize', { fontSize: size }).run();
        },
    } as Partial<RawCommands>;
  },
});

export default FontSize; 