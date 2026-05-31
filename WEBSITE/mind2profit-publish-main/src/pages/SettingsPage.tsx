import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth, type UserPreferences } from "@/contexts/AuthContext";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { ArrowLeft, CreditCard, User, Bell, Wallet } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";

const Plans = [
  { id: "pro", label: "Pro" },
  { id: "premium", label: "Premium" },
  { id: "enterprise", label: "Enterprise" },
] as const;

const SettingsPage = () => {
  const {
    user,
    preferences,
    plan,
    isSubscribed,
    updateDisplayName,
    updatePreferences,
    updateBilling,
    upgrade,
  } = useAuth();
  const { toast } = useToast();
  const [name, setName] = useState(user?.name || "");
  const [savingProfile, setSavingProfile] = useState(false);
  const [savingPrefs, setSavingPrefs] = useState(false);
  const [savingBilling, setSavingBilling] = useState(false);
  const [savingPlan, setSavingPlan] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(plan && plan !== "none" ? plan : "pro");

  const [bill, setBill] = useState<Pick<
    UserPreferences,
    "billingName" | "billingLine1" | "billingLine2" | "billingCity" | "billingRegion" | "billingPostal" | "billingCountry"
  >>({
    billingName: preferences.billingName,
    billingLine1: preferences.billingLine1,
    billingLine2: preferences.billingLine2,
    billingCity: preferences.billingCity,
    billingRegion: preferences.billingRegion,
    billingPostal: preferences.billingPostal,
    billingCountry: preferences.billingCountry,
  });

  useEffect(() => {
    setName(user.name);
    setBill({
      billingName: preferences.billingName,
      billingLine1: preferences.billingLine1,
      billingLine2: preferences.billingLine2,
      billingCity: preferences.billingCity,
      billingRegion: preferences.billingRegion,
      billingPostal: preferences.billingPostal,
      billingCountry: preferences.billingCountry,
    });
  }, [user.id, user.name, preferences]);

  useEffect(() => {
    if (plan && plan !== "none") setSelectedPlan(plan);
  }, [plan]);

  if (!user) {
    return null;
  }

  const expires = user.subscription?.expiresAt
    ? new Date(user.subscription.expiresAt)
    : null;

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingProfile(true);
    try {
      await updateDisplayName(name.trim() || user.email);
      toast({ title: "Profile updated", description: "Your display name is saved to your account." });
    } catch (err: unknown) {
      toast({ title: "Error", description: (err as Error).message, variant: "destructive" });
    } finally {
      setSavingProfile(false);
    }
  };

  const savePrefs = async (patch: Partial<UserPreferences>) => {
    setSavingPrefs(true);
    try {
      await updatePreferences(patch);
      toast({ title: "Notification preferences saved" });
    } catch (err: unknown) {
      toast({ title: "Error", description: (err as Error).message, variant: "destructive" });
    } finally {
      setSavingPrefs(false);
    }
  };

  const saveBilling = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingBilling(true);
    try {
      await updateBilling(bill);
      toast({ title: "Billing details saved" });
    } catch (err: unknown) {
      toast({ title: "Error", description: (err as Error).message, variant: "destructive" });
    } finally {
      setSavingBilling(false);
    }
  };

  const handlePlanUpdate = async () => {
    if (selectedPlan === (plan || "none")) {
      toast({ title: "No change", description: "Pick a different plan or use Upgrade to compare." });
      return;
    }
    setSavingPlan(true);
    try {
      await upgrade(selectedPlan);
      toast({ title: "Plan updated", description: "Your plan metadata has been updated." });
    } catch (err: unknown) {
      toast({ title: "Error", description: (err as Error).message, variant: "destructive" });
    } finally {
      setSavingPlan(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" asChild>
            <Link to={isSubscribed ? "/dashboard" : "/"} className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back
            </Link>
          </Button>
          <h1 className="text-2xl font-bold">Settings</h1>
        </div>

        <Tabs defaultValue="profile" className="w-full">
          <TabsList className="grid w-full grid-cols-4 h-auto flex-wrap sm:flex-nowrap">
            <TabsTrigger value="profile" className="gap-1">
              <User className="h-3.5 w-3.5" />
              Profile
            </TabsTrigger>
            <TabsTrigger value="notifications" className="gap-1">
              <Bell className="h-3.5 w-3.5" />
              Notifications
            </TabsTrigger>
            <TabsTrigger value="plan" className="gap-1">
              <Wallet className="h-3.5 w-3.5" />
              Plan
            </TabsTrigger>
            <TabsTrigger value="billing" className="gap-1">
              <CreditCard className="h-3.5 w-3.5" />
              Billing
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Profile</CardTitle>
                <CardDescription>Update how your name appears in Mind2Profit.</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleProfileSave} className="space-y-4 max-w-md">
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" value={user.email} disabled className="mt-1 bg-muted" />
                    <p className="text-xs text-muted-foreground mt-1">Sign-in email (managed by your auth provider).</p>
                  </div>
                  <div>
                    <Label htmlFor="name">Display name</Label>
                    <Input
                      id="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="mt-1"
                    />
                  </div>
                  <Button type="submit" disabled={savingProfile}>
                    {savingProfile ? "Saving…" : "Save profile"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Notifications</CardTitle>
                <CardDescription>
                  In-app notifications appear in the bell in the top bar. End-of-day P&L and journal reminders use your journal
                  and backend schedule; email reminders are configured on the server.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium">End-of-day P&L</p>
                    <p className="text-sm text-muted-foreground">
                      After 4:00 PM local, show today&apos;s P&L from your journal in notifications.
                    </p>
                  </div>
                  <Switch
                    checked={preferences.notifyEodPnl}
                    onCheckedChange={(v) => void savePrefs({ notifyEodPnl: v })}
                    disabled={savingPrefs}
                  />
                </div>
                <Separator />
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium">Journal reminder</p>
                    <p className="text-sm text-muted-foreground">Daily in-app nudge to complete your journal.</p>
                  </div>
                  <Switch
                    checked={preferences.notifyJournalReminder}
                    onCheckedChange={(v) => void savePrefs({ notifyJournalReminder: v })}
                    disabled={savingPrefs}
                  />
                </div>
                <div>
                  <Label htmlFor="remindTime">Reminder time (local, 24h)</Label>
                  <div className="flex flex-wrap items-end gap-2 mt-1">
                    <Input
                      id="remindTime"
                      type="time"
                      className="w-40"
                      defaultValue={preferences.journalReminderTime}
                      key={preferences.journalReminderTime}
                      onBlur={(e) => {
                        if (e.target.value && e.target.value !== preferences.journalReminderTime) {
                          void savePrefs({ journalReminderTime: e.target.value });
                        }
                      }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="plan" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Plan & subscription</CardTitle>
                <CardDescription>Your plan is stored on your user profile. For production, connect Stripe or your billing system.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm text-muted-foreground">Status:</span>
                  {isSubscribed ? <Badge>Active</Badge> : <Badge variant="secondary">Not subscribed</Badge>}
                  {plan && plan !== "none" && (
                    <span className="text-sm">
                      Plan: <strong className="capitalize">{plan}</strong>
                    </span>
                  )}
                </div>
                {expires && isSubscribed && (
                  <p className="text-sm text-muted-foreground">
                    Next renewal reference: {expires.toLocaleString()}
                  </p>
                )}
                <div className="max-w-xs space-y-2">
                  <Label htmlFor="planSelect">Change plan (metadata)</Label>
                  <select
                    id="planSelect"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={selectedPlan}
                    onChange={(e) => setSelectedPlan(e.target.value)}
                  >
                    {Plans.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button onClick={handlePlanUpdate} disabled={savingPlan || !isSubscribed}>
                    {savingPlan ? "Saving…" : "Apply plan to account"}
                  </Button>
                  <Button variant="outline" asChild>
                    <Link to="/upgrade">Compare on Upgrade page</Link>
                  </Button>
                </div>
                {!isSubscribed && (
                  <p className="text-sm text-amber-600">Subscribe first to apply a live plan, or use Upgrade to choose a plan.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="billing" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Billing & invoices</CardTitle>
                <CardDescription>
                  Billing contact and address for your account. Card payments and invoices are not stored in this app — wire up
                  Stripe/portal when ready. Receipts go to your sign-in email unless you add a billing contact.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={saveBilling} className="space-y-4 max-w-lg">
                  <p className="text-sm text-muted-foreground">Invoice / receipt email: {user.email}</p>
                  <Separator />
                  <div>
                    <Label htmlFor="bname">Name on account</Label>
                    <Input
                      id="bname"
                      value={bill.billingName}
                      onChange={(e) => setBill((b) => ({ ...b, billingName: e.target.value }))}
                    />
                  </div>
                  <div>
                    <Label htmlFor="b1">Address line 1</Label>
                    <Input
                      id="b1"
                      value={bill.billingLine1}
                      onChange={(e) => setBill((b) => ({ ...b, billingLine1: e.target.value }))}
                    />
                  </div>
                  <div>
                    <Label htmlFor="b2">Address line 2</Label>
                    <Input
                      id="b2"
                      value={bill.billingLine2}
                      onChange={(e) => setBill((b) => ({ ...b, billingLine2: e.target.value }))}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label htmlFor="bcity">City</Label>
                      <Input
                        id="bcity"
                        value={bill.billingCity}
                        onChange={(e) => setBill((b) => ({ ...b, billingCity: e.target.value }))}
                      />
                    </div>
                    <div>
                      <Label htmlFor="breg">State / region</Label>
                      <Input
                        id="breg"
                        value={bill.billingRegion}
                        onChange={(e) => setBill((b) => ({ ...b, billingRegion: e.target.value }))}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label htmlFor="bpost">Postal code</Label>
                      <Input
                        id="bpost"
                        value={bill.billingPostal}
                        onChange={(e) => setBill((b) => ({ ...b, billingPostal: e.target.value }))}
                      />
                    </div>
                    <div>
                      <Label htmlFor="bcountry">Country</Label>
                      <Input
                        id="bcountry"
                        value={bill.billingCountry}
                        onChange={(e) => setBill((b) => ({ ...b, billingCountry: e.target.value }))}
                      />
                    </div>
                  </div>
                  <Button type="submit" disabled={savingBilling}>
                    {savingBilling ? "Saving…" : "Save billing information"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default SettingsPage;
