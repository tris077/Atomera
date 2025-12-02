declare module '3dmol' {
  export interface ViewerConfig {
    backgroundColor?: string;
  }

  export interface SurfaceType {
    VDW: number;
    MS: number;
    SAS: number;
    SES: number;
  }

  export interface Viewer {
    addModel(data: string, format: string): void;
    setStyle(selection: any, style: any): void;
    addSurface(type: number, style: any, selection: any): void;
    removeAllSurfaces(): void;
    zoomTo(selection?: any, animationDuration?: number): void;
    zoom(factor: number, animationDuration?: number): void;
    render(): void;
    clear(): void;
  }

  export function createViewer(element: HTMLElement, config: ViewerConfig): Viewer;
}

declare global {
  interface Window {
    $3Dmol: {
      createViewer: (element: HTMLElement, config: any) => any;
      SurfaceType: {
        VDW: number;
        MS: number;
        SAS: number;
        SES: number;
      };
    };
  }
}

export {};
