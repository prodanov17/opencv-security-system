import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { useState } from "react";

export function SwitchDemo({
  armed,
  label,
  callback,
}: {
  label: string;
  armed: boolean;
  callback: (checked: boolean) => void;
}) {
  return (
    <div className="flex items-center space-x-2">
      <Switch
        id="airplane-mode"
        checked={armed}
        onCheckedChange={() => {
          callback(!armed);
        }}
      />
      <Label htmlFor="airplane-mode">{label}</Label>
    </div>
  );
}
