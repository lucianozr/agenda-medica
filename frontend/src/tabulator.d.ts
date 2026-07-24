declare module 'tabulator-tables' {
  interface TabulatorOptions {
    [key: string]: any
  }

  class Tabulator {
    constructor(element: HTMLElement | string, options?: TabulatorOptions)
    replaceData(data: unknown[]): void
    destroy(): void
  }

  export const TabulatorFull: typeof Tabulator
  export default Tabulator
}
