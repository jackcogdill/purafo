export class Keyboard {
  private readonly map = new Map<string, boolean>();

  listen() {
    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);
  }

  unlisten() {
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);

    // Reset all keys
    for (const key of this.map.keys()) {
      this.map.set(key, false);
    }
  }

  listenForKeys(keys: string[]) {
    this.listen();
    for (const key of keys) {
      this.map.set(key, false);
    }
  }

  private onKeyDown(e: KeyboardEvent) {
    const {key} = e;
    if (!this.map.has(key))
      return;
    e.preventDefault();
    this.map.set(key, true);
  }

  private onKeyUp(e: KeyboardEvent) {
    const {key} = e;
    if (!this.map.has(key))
      return;
    e.preventDefault();
    this.map.set(key, false);
  }

  private isKeyDown(key: string): boolean {
    const value = this.map.get(key);
    if (value === undefined) {
      throw new Error(`Key '${key}' is not being listened to`);
    }
    return value;
  }

  isDown(keys: string|string[]): boolean {
    return typeof keys === 'string' ? this.isKeyDown(keys)
                                    : keys.some(key => this.isKeyDown(key));
  }
}

export const Keys = {
  ENTER : 'Enter',
  ESC : 'Escape',
  UP : 'ArrowUp',
  DOWN : 'ArrowDown',
  LEFT : 'ArrowLeft',
  RIGHT : 'ArrowRight',
  K0 : '0',
  K1 : '1',
  K2 : '2',
  K3 : '3',
  K4 : '4',
  K5 : '5',
  K6 : '6',
  K7 : '7',
  K8 : '8',
  K9 : '9',
  A : 'a',
  B : 'b',
  C : 'c',
  D : 'd',
  E : 'e',
  F : 'f',
  G : 'g',
  H : 'h',
  I : 'i',
  J : 'j',
  K : 'k',
  L : 'l',
  M : 'm',
  N : 'n',
  O : 'o',
  P : 'p',
  Q : 'q',
  R : 'r',
  S : 's',
  T : 't',
  U : 'u',
  V : 'v',
  W : 'w',
  X : 'x',
  Y : 'y',
  Z : 'z',
};
